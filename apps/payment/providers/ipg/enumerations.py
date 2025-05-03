from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class GatewayProviderEnum(TextChoices):
    ZARRINPAL = ('ZARRINPAL', _('ZarrinPal'))
    MELLAT = ('MELLAT', _('Mellat Bank'))
