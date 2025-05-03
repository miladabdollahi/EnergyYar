from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.core.viewsets import CoreViewSet
from apps.payment.models import Payment
from apps.wallet.serializers import WalletPublicPaySerializer

wallet_services = use('apps.wallet.services')


class WalletPublicViewSet(CoreViewSet):
    serializers = {
        'pay': WalletPublicPaySerializer
    }

    @action(methods=['POST'], detail=False)
    def pay(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_slug = serializer.validated_data.get('payment_slug')
        payment = get_object_or_404(Payment, slug=payment_slug)

        amount = serializer.validated_data.get('amount')
        platform = serializer.validated_data.get('platform')
        route = serializer.validated_data.get('route')
        use_wallet = serializer.validated_data.get('use_wallet')
        wallet_balance = serializer.validated_data.get('wallet_balance')
        data = wallet_services.pay(
            payment, amount, request, platform, route,
            use_wallet=use_wallet, wallet_balance=wallet_balance
        )

        return Response(data)
