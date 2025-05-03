from django.db import transaction as db_transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.core.structs import Manager
from apps.payment.models import Transaction, Payment
from apps.service_manager.hooks import register_service, use
from apps.wallet.models import Wallet

transaction_services = use('apps.payment.service', 'transaction')
payment_services = use('apps.payment.service', 'payment')


class WalletCoreManager(Manager):

    @staticmethod
    def get_wallet(raise_exception=False, **filters):
        """
        gets the wallet of given user.

        :param bool raise_exception: raise exception.

        :raises ValidationError: wallet not found error.

        :rtype: Wallet
        """

        try:
            return Wallet.objects.get(**filters)
        except Wallet.DoesNotExist:
            if raise_exception:
                raise ValidationError(
                    _('Wallet with this [{filters}] filters not found.').format(filters=filters)
                )
        except Wallet.MultipleObjectsReturned:
            if raise_exception:
                raise ValidationError(
                    _(
                        'Wallet with this [{filters}] filters don`t be unique.'
                    ).format(filters=filters)
                )


@register_service()
class WalletManager(WalletCoreManager):

    def pay(self, payment, paying_user, paying_amount, destination_account, display_wallet_balance):
        """
        pay by wallet.

        :param apps.payment.models.Payment payment: payment instance.
        :param apps.user.models.User paying_user: paying user instance.
        :param int paying_amount: amount to pay.
        :param object destination_account: destination account.
        :param int display_wallet_balance: wallet balance that shown to user.
        """

        wallet = self.get_wallet(user=paying_user, raise_exception=True)
        if (
                display_wallet_balance is None or
                display_wallet_balance < 0 or
                display_wallet_balance != wallet.balance
        ):
            raise ValidationError(_('Wallet balance has been changed. please update data.'))

        if paying_amount > wallet.balance:
            raise ValidationError(_('Wallet balance, not enough.'))

        with db_transaction.atomic():
            transaction = transaction_services.create_transaction(
                payment=payment, source_account=wallet, destination_account=destination_account,
                amount=paying_amount, through=Transaction.ThroughChoice.WALLET.value
            )

            self.decrease_balance(wallet, paying_amount)

            transaction_services.update_transaction(
                transaction, status=Transaction.StatusChoice.SUCCESS.value
            )

            if payment.remaining_of_payment <= 0:
                payment_services.update_payment(payment, status=Payment.StatusChoice.CLEARED.value)

    @staticmethod
    def __change_balance(wallet, amount):
        """
        changes the given wallet balance.

        :param Wallet wallet: wallet instance to increase its balance.
        :param int amount: changing amount.
        """

        wallet.balance = F('balance') + amount
        wallet.save(update_fields=['balance'])

    def increase_balance(self, wallet, amount):
        """
        increase the given wallet balance.

        :param Wallet wallet: wallet instance to increase its balance.
        :param int amount: increasing amount.
        """

        return self.__change_balance(wallet, amount)

    def decrease_balance(self, wallet, amount):
        """
        decreases the given wallet balance.

        :param Wallet wallet: wallet instance to decrease its balance.
        :param int amount: decreasing amount.
        """

        return self.__change_balance(wallet, -amount)
