import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils.translation import gettext_lazy as _


def generate_tracking_code():
    return int(str(uuid.uuid4().int)[-1 * 64:])


class PaymentItem(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Payment(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = ('pending', _('Pending'))
        CLEARED = ('cleared', _('Cleared'))
        CANCELED = ('canceled', _('Canceled.'))
        FAILED = ('failed', _('Failed'))

    class ReasonChoice(models.TextChoices):
        PENDING = ('pending', _('Pending'))
        CLEARED = ('cleared', _('Cleared'))
        CANCELED = ('canceled', _('Canceled.'))
        FAILED = ('failed', _('Failed'))

    amount = models.PositiveBigIntegerField()
    issuer_user = models.ForeignKey(
        'user.User', on_delete=models.PROTECT, related_name='payment_issuer_user'
    )

    item = models.ForeignKey(
        'PaymentItem', on_delete=models.PROTECT, null=True, blank=True,
        related_name='payments'
    )
    reason = models.CharField(choices=ReasonChoice)
    status = models.CharField(choices=StatusChoice, default=StatusChoice.PENDING.value)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    @property
    def paid_amount(self):
        if self.id is not None:
            self.result = Transaction.objects.filter(
                payment=self, status=Transaction.StatusChoice.SUCCESS.value
            ).aggregate(paid=models.Sum('amount'))
            return self.result.get('paid') or 0


class TransactionAccount(models.Model):
    """
    Transaction account (BankAccount, Wallet)
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Transaction(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING = ('pending', _('Pending'))
        SUCCESS = ('success', _('Success'))
        FAILED = ('failed', _('Failed'))
        REDIRECT_TO_BANK = ('redirect_to_bank', _('Redirect to Bank'))
        RETURN_FROM_BANK = ('return_from_bank', _('Return from Bank'))
        CANCELED_BY_USER = ('canceled_by_user', _('Canceled by User'))
        GATEWAY_TOKEN_EXPIRED = ('gateway_token_expired', _('Gateway Token Expired'))
        PAYMENT_VERIFICATION_EXPIRED = (
            'payment_verification_expired', _('Payment Verification Expired')
        )

        @classmethod
        def canceled(cls):
            return cls.CANCELED_BY_USER, cls.GATEWAY_TOKEN_EXPIRED, cls.PAYMENT_VERIFICATION_EXPIRED

    class ThroughChoice(models.TextChoices):
        GATEWAY = ('gateway', _('Gateway'))
        WALLET = ('wallet', _('Wallet'))
        IMAGE = ('image', _('Image'))

    payment = models.ForeignKey(
        'payment.Payment', on_delete=models.PROTECT, related_name='transactions'
    )

    source_account = models.ForeignKey(
        'TransactionAccount', on_delete=models.PROTECT, related_name='source_transactions'
    )

    destination_account = models.ForeignKey(
        'TransactionAccount', on_delete=models.PROTECT, related_name='destination_transactions'
    )

    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=32, choices=StatusChoice, default=StatusChoice.PENDING.value)
    through = models.CharField(
        max_length=32, choices=ThroughChoice, default=ThroughChoice.GATEWAY.value
    )

    tracking_code = models.CharField(max_length=64, unique=True, default=generate_tracking_code)
    reference_number = models.CharField(max_length=256, null=True, blank=True)

    response_result = models.TextField(null=True, blank=True)
    callback_url = models.TextField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    payment_time = models.DateTimeField(blank=True, null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Gateway(models.Model):
    class ModeChoice(models.TextChoices):
        ONLINE = ('online', _('Online'))
        OFFLINE = ('offline', _('Offline'))

    class TypeChoice(models.TextChoices):
        PSP = ('PSP', _('Payment service provider.'))
        IPG = ('IPG', _('Internet payment gateway.'))

    title = models.CharField(max_length=128)
    mode = models.CharField(max_length=32, choices=ModeChoice)
    type = models.CharField(max_length=32, choices=TypeChoice)

    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    card_number = models.CharField(max_length=32, null=True, blank=True)
    account_number = models.CharField(max_length=32, null=True, blank=True)
    iban = models.CharField(max_length=32, null=True, blank=True)
    bank = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(max_length=256, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    @property
    def default_online_ipg(self):
        return self.objects.get(
            mode=self.ModeChoice.ONLINE.value, type=self.TypeChoice.IPG.value, is_default=True
        )
