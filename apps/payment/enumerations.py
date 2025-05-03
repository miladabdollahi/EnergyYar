from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class PlatformChoice(TextChoices):
    BACK_OFFICE = 'back_office'
    PWA = 'pwa'


class CurrencyChoice(TextChoices):
    IRR = ('IRR', _('Rial'))
    IRT = ('IRT', _('Toman'))


MIN_PAYMENT_AMOUNT = 1_000
MAX_PAYMENT_AMOUNT = 50_000_000
MAX_UPLOADED_IMAGE = 30