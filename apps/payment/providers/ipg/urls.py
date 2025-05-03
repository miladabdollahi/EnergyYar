from django.urls import path

from apps.payment.providers.ipg.apps import IPGProvidersConfig
from apps.payment.providers.ipg.views import return_from_gateway

_urlpatterns = [
    # path('redirect-to-gateway/', redirect_to_gateway, name='redirect-to-gateway'),
    path('return-from-gateway/', return_from_gateway, name='return-from-gateway'),
]


def get_ipg_provider_urls():
    return _urlpatterns, IPGProvidersConfig.name, IPGProvidersConfig.name
