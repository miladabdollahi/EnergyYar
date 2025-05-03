from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.payment.tests.factories import PaymentFactory, GatewayFactory
from apps.payment.models import Gateway
from apps.user.tests.factories import UserFactory
from apps.payment.enumerations import PlatformChoice
from apps.wallet.tests.factories import WalletFactory

class PaymentPublicViewSet(APITestCase):

    def test_pay(self):
        requested_user = UserFactory(is_superuser=True)
        self.client.force_authenticate(requested_user)

        WalletFactory(user=requested_user)
        GatewayFactory(
            mode=Gateway.ModeChoice.ONLINE.value, type=Gateway.TypeChoice.IPG.value,
            is_default=True, slug='ZARRINPAL'
        )
        payment = PaymentFactory()
        url = reverse('v1:PaymentPublic-pay')
        response = self.client.post(
            url,
            dict(
                amount=payment.amount,
                payment_slug=payment.slug,
                route='/',
                platform=PlatformChoice.BACK_OFFICE.value
            ),
            format='json'
        )
        self.assertEqual(url, f'/api/v1/payments/pay/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
