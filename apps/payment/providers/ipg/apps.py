from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class IPGProvidersConfig(AppConfig):
    name = 'apps.payment.providers.ipg'
    verbose_name = _('Iranian bank gateway')
    verbose_name_plural = _('Iranian bank gateways')
    default_auto_field = 'django.db.models.BigAutoField'
