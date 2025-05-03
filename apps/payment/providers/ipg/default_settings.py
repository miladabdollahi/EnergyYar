"""
default settings for gateways.
"""

from django.conf import settings

from apps.payment.providers.ipg.apps import IPGProvidersConfig

IPG_PROVIDERS_CONFIG = getattr(
    settings,
    'IPG_PROVIDERS_CONFIG',
    {
        'ZARRINPAL': {
            'class': 'apps.payment.providers.ipg.handlers.zarrinpal.Zarrinpal',
            'info': {
                'MERCHANT_CODE': '<Zarrinpal merchant code (MERCHANT_ID)>'
            },
            'config': {
                'GATEWAY_CLIENT': '<Zarrinpal gateway client (wsdl url)>'
            }
        },
        'MELLAT': {
            'class': 'apps.payment.providers.ipg.handlers.mellat.Mellat'
        }
    }
)

_IPG_CONFIG = getattr(
    settings,
    'IPG_CONFIG',
    {
        'PRIORITIES': [],
        'DEFAULT': 'ZARRINPAL',
        'SETTING_VALUE_READER_CLASS': 'apps.payment.providers.ipg.readers.default.DefaultReader',
        'CURRENCY': 'IRR',
        'TRACKING_CODE_QUERY_PARAM': 'tc',
        'TRACKING_CODE_LENGTH': 16,
        'IS_SAMPLE_FORM_ENABLE': False,
        'CALLBACK_NAMESPACE': f'{IPGProvidersConfig.name}:return-from-gateway'
    }
)
BANK_PRIORITIES = _IPG_CONFIG.get('PRIORITIES', [])
IPG_DEFAULT = _IPG_CONFIG.get('DEFAULT', 'ZARRINPAL')
SETTING_VALUE_READER_CLASS = _IPG_CONFIG.get(
    'SETTING_VALUE_READER_CLASS', 'apps.payment.providers.ipg.readers.default.DefaultReader'
)
CURRENCY = _IPG_CONFIG.get('CURRENCY', 'IRR')
TRACKING_CODE_QUERY_PARAM = _IPG_CONFIG.get('TRACKING_CODE_QUERY_PARAM', 'tc')
TRACKING_CODE_LENGTH = _IPG_CONFIG.get('TRACKING_CODE_LENGTH', 16)
IS_SAMPLE_FORM_ENABLE = _IPG_CONFIG.get('IS_SAMPLE_FORM_ENABLE', False)
CALLBACK_NAMESPACE = _IPG_CONFIG.get(
    'CALLBACK_NAMESPACE', f'{IPGProvidersConfig.name}:return-from-gateway'
)
# GO_TO_BANK_NAMESPACE = _IPG_CONFIG.get(
#     'GO_TO_BANK_NAMESPACE', f'{IPGProvidersConfig.name}:redirect-to-gateway'
# )