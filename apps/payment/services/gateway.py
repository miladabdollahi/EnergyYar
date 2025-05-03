from rest_framework.exceptions import ValidationError

from apps.core.structs import Manager
from apps.core.utils import generate_standard_mobile_number
from django.utils.translation import gettext_lazy as _
from apps.payment.models import Gateway
from apps.payment.providers.ipg.factory import IPGFactory
from apps.service_manager.hooks import register_service


class GatewayCoreManager(Manager):
    @staticmethod
    def get_gateway(raise_exception=False, **filters):
        """
        get gateway.

        :rtype: Gateway
        """

        try:
            return Gateway.objects.get(**filters)
        except Gateway.DoesNotExist:
            if raise_exception:
                raise ValidationError(
                    _('Gateway with this [{filters}] filters not found.').format(filters=filters)
                )
        except Gateway.MultipleObjectsReturned:
            if raise_exception:
                raise ValidationError(
                    _(
                        'Gateway with this [{filters}] filters don`t be unique.'
                    ).format(filters=filters)
                )


@register_service('gateway')
class GatewayManager(GatewayCoreManager):
    @staticmethod
    def generate_client_callback_url(platform, route):
        return ''

    def get_gateway_url(self, payment, paying_user, paying_amount, platform, route, **kwargs):
        """
        gets the gateway url for payment.

        :param apps.payment.models.Payment payment: payment instance.
        :param apps.user.models.User paying_user: paying user instance.
        :param int paying_amount: amount to pay.
        :param int platform: application platform.
        :param str route: application route.

        :rtype: str
        """

        factory = IPGFactory()
        gateway = factory.create()
        gateway.set_paying_user(paying_user)
        gateway.set_paying_amount(paying_amount)
        gateway.set_platform(platform)
        client_callback = self.generate_client_callback_url(platform, route)
        gateway.set_client_callback_url(client_callback)
        standard_mobile = generate_standard_mobile_number(paying_user.mobile)
        if standard_mobile is not None:
            gateway.set_mobile_number(standard_mobile)

        return gateway.pay(payment)
