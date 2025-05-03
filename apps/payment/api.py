from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from apps.security.authentication.authenticators import IsSuperuserAuthenticated
from apps.core.viewsets import CoreViewSet
from apps.payment.models import Payment
from apps.service_manager.hooks import use
from apps.payment.serializers import GatewayPaySerializer

payment_services = use('apps.payment.services', 'payment')


class PaymentPublicViewSet(CoreViewSet):
    permission_classes = IsSuperuserAuthenticated

    serializers = {
        'pay': GatewayPaySerializer
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
        data = payment_services.pay(payment, request.user, amount, platform, route)

        return Response(data)
