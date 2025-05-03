from rest_framework import routers

from apps.payment.api import PaymentPublicViewSet

v1_router = routers.DefaultRouter()
v1_router.register('payments', PaymentPublicViewSet, 'PaymentPublic')

