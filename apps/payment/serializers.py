from rest_framework import serializers

from apps.payment.enumerations import PlatformChoice


class GatewayPaySerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=False, min_value=1, allow_null=True)
    payment_slug = serializers.CharField(required=True, allow_null=False)
    route = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    platform = serializers.ChoiceField(
        choices=PlatformChoice, required=True, allow_null=False, allow_blank=False
    )
