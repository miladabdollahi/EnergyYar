from django.db.models.aggregates import Sum
from rest_framework.exceptions import ValidationError

from apps.core.structs import Manager
from django.utils.translation import gettext_lazy as _
from apps.core.utils import make_iterable
from apps.payment.models import Transaction, TransactionAccount
from apps.service_manager.hooks import register_service, use

wallet_services = use('apps.wallet.services')
gateway_services = use('apps.payment.gateway.services', 'gateway')
payment_services = use('apps.payment.services', 'payment')

MIN_PAYMENT_AMOUNT = 1000
MAX_PAYMENT_AMOUNT = 200000000
MAX_UPLOADED_IMAGE = 30


class TransactionCoreManager(Manager):
    @staticmethod
    def get_transaction(raise_exception=False, **filters):
        """
        gets the wallet of given user.

        :param bool raise_exception: raise exception.

        :raises ValidationError: wallet not found error.

        :rtype: Transaction
        """

        try:
            return Transaction.objects.get(**filters)
        except Transaction.DoesNotExist:
            if raise_exception:
                raise ValidationError(
                    _('Transaction with this [{filters}] filters not found.').format(
                        filters=filters)
                )
        except Transaction.MultipleObjectsReturned:
            if raise_exception:
                raise ValidationError(
                    _(
                        'Transaction with this [{filters}] filters don`t be unique.'
                    ).format(filters=filters)
                )

    @staticmethod
    def update_transaction(transaction, **kwargs):
        """
        update transaction.

        :param Transaction transaction: transaction instance.
        """

        update_fields = ['modified_time']
        for key, value in kwargs.items():
            setattr(transaction, key, value)
            update_fields.append(key)

        transaction.save(update_fields=update_fields)

    @staticmethod
    def create_transaction(payment, source_account, destination_account, amount, **kwargs):
        """
        create transaction.

        :param apps.payment.models.Payment payment: payment instance.
        :param apps.payment.models.TransactionAccount source_account: source account instance.
        :param apps.payment.models.TransactionAccount destination_account:
        destination account instance.
        :param int amount: amount to pay.

        :keyword str through: through paying.

        :rtype: Transaction
        """

        if source_account is not None:
            kwargs.update(
                source_account=TransactionAccount.objects.create(
                    content_object=source_account
                )
            )

        if destination_account is not None:
            kwargs.update(
                destination_account=TransactionAccount.objects.create(
                    content_object=destination_account
                )
            )

        return Transaction.objects.create(payment=payment, amount=amount, **kwargs)


@register_service('transaction')
class TransactionManager(TransactionCoreManager):

    @staticmethod
    def get_paid_amount(payment, **kwargs):
        """
        gets the paid amount of given payment.

        :keyword int | list[int] | tuple[int] status: payment paid in this status.
        :keyword boolean is_approved: transactions that approved.
        :keyword Payment payment: payment instance.

        :rtype: int
        """

        filters = dict()

        status = kwargs.pop('status', Transaction.StatusChoice.SUCCESS.value)

        if payment is not None:
            filters.update(payment=payment)

        status = make_iterable(status)

        result = Transaction.objects.filter(
            payment=payment, status__in=status, **filters
        ).aggregate(paid=Sum('amount'))

        return result.get('paid') or 0
