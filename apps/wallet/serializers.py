from rest_framework import serializers
from apps.payment.enumerations import PlatformChoice
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class WalletPublicPaySerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=False, min_value=1, allow_null=True)
    payment_slug = serializers.CharField(required=True, allow_null=False)
    route = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    platform = serializers.ChoiceField(
        choices=PlatformChoice, required=True, allow_null=False, allow_blank=False
    )
    use_wallet = serializers.BooleanField(required=False, allow_null=False)
    wallet_balance = serializers.IntegerField(required=False, allow_null=False)

    def validate(self, attrs):
        use_wallet = attrs.get('use_wallet')
        wallet_balance = attrs.get('wallet_balance')
        if use_wallet and wallet_balance is None:
            raise ValidationError({'wallet_balance': _('This field is required.')})

        return attrs
