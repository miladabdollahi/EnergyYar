from rest_framework.exceptions import ValidationError

from apps.core.structs import Manager
from django.utils.translation import gettext_lazy as _
from apps.payment.enumerations import MAX_PAYMENT_AMOUNT
from apps.payment.models import Payment
from apps.service_manager.hooks import register_service, use

wallet_services = use('apps.wallet.services')
transaction_services = use('apps.payment.services', 'transaction')
gateway_services = use('apps.payment.services', 'gateway')


class PaymentCoreManager(Manager):
    @staticmethod
    def update_payment(payment, **kwargs):
        """
        update payment.

        :rtype: Payment
        """

        update_fields = ['modified_time']
        for key, value in kwargs.items():
            setattr(payment, key, value)
            update_fields.append(key)

        payment.save(update_fields=update_fields)


@register_service('payment')
class PaymentManager(PaymentCoreManager):

    @staticmethod
    def get_rials(amount):
        """
        gets the rials equivalent of given tomans amount.

        :param int amount: amount in tomans.

        :rtype: int
        """

        return amount * 10

    @staticmethod
    def get_tomans(amount):
        """
        gets the tomans equivalent of given rials amount.

        :param int amount: amount in rials.

        :rtype: int
        """

        result = amount / 10
        if int(result) == result:
            return int(result)

        return result

    def pay(self, payment, paying_user, paying_amount, platform, route, **kwargs):
        """
        pays a payment using online gateway.

        :param apps.payment.models.Payment payment: payment instance.
        :param apps.user.models.User paying_user: paying user instance.
        :param int paying_amount: amount to pay.
        :param int platform: application platform.
        :param str route: application route.

        :return: dict(
            str url: gateway url,
            bool redirect_to_gateway: client should be redirected to gateway,
            gateway_amount: amount to be paid using gateway
        )
        :rtype: dict
        """

        if paying_amount > MAX_PAYMENT_AMOUNT:
            raise ValidationError(
                _(
                    'The payment amount is more than a single transaction limit. '
                    'Please allow your wallet balance to also be used for payment.'
                )
            )

        if payment.status != Payment.StatusChoice.PENDING.value:
            raise ValidationError(
                _(
                    'Payment [{payment}] is in [{status}] status and could not be progressed.'
                ).format(payment=payment.slug, status=Payment.StatusChoice(payment.status))
            )

        remaining_of_payment = payment.amount - payment.paid_amount

        if remaining_of_payment <= 0:
            raise ValidationError(
                _('Payment [{payment}] is cleared.').format(payment=payment.slug)
            )

        if paying_amount > payment.amount or paying_amount > remaining_of_payment:
            raise ValidationError(
                _(
                    'Provided amount [{amount}] is bigger than the remaining '
                    'amount of payment [{payment}].'
                ).format(payment=payment.slug, amount=paying_amount)
            )

        url = gateway_services.get_gateway_url(
            payment, paying_user, paying_amount, platform, route, **kwargs
        )

        return dict(url=url, redirect_to_gateway=True, paying_amount=paying_amount)
