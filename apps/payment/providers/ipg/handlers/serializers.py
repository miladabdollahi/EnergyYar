from rest_framework import serializers


class MellatVerifySerializer(serializers.Serializer):
    RefId = serializers.CharField(required=True, allow_null=False)
    SaleOrderId = serializers.CharField(required=True, allow_null=False)
    FinalAmount = serializers.IntegerField(required=False, allow_null=True)
    ResCode = serializers.CharField(required=False, allow_null=True)
    SaleReferenceId = serializers.IntegerField(required=False, allow_null=True)
    CardHolderPAN = serializers.CharField(required=False, allow_null=True)
    CardHolderInfo = serializers.CharField(required=False, allow_null=True)
