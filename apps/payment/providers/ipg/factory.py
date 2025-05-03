import importlib


class IPGFactory:

    def __init__(self):
        from apps.payment.providers.ipg import default_settings
        self._secret_value_reader = self._import(default_settings.SETTING_VALUE_READER_CLASS)()

    @staticmethod
    def _import(path):
        package, attr = path.rsplit('.', 1)
        return getattr(importlib.import_module(package), attr)

    def _import_provider(self, provider_type):
        """
        helper to import bank aliases from string paths.

        raises an AttributeError if a bank can't be found by it's alias
        """
        bank_class = self._import(self._secret_value_reader.get_class(provider_type=provider_type))

        return bank_class, self._secret_value_reader.read(provider_type=provider_type)

    def create(self, provider_type=None):
        """Build provider class"""

        if not provider_type:
            provider_type = self._secret_value_reader.default()

        provider_class, provider_settings = self._import_provider(provider_type)
        return provider_class(**provider_settings)
