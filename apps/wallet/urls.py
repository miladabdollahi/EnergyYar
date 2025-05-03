from rest_framework import routers

from apps.wallet.api import WalletPublicViewSet

v1_router = routers.DefaultRouter()
v1_router.register('wallets', WalletPublicViewSet, 'WalletPublic')
