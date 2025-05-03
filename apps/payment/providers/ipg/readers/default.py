from apps.payment.providers.ipg import default_settings as settings
from apps.payment.providers.ipg.readers.base import ReaderBase


class DefaultReader(ReaderBase):

    def read(self, provider_type, **options):
        return dict(
            info=settings.IPG_PROVIDERS_CONFIG.get(provider_type).get('info'),
            config=settings.IPG_PROVIDERS_CONFIG.get(provider_type).get('config')
        )

    def get_class(self, provider_type, **options):
        return settings.IPG_PROVIDERS_CONFIG.get(provider_type).get('class')

    def default(self):
        return settings.IPG_DEFAULT
