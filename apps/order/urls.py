from rest_framework import routers

from apps.order.api import OrderViewSet

v1_router = routers.DefaultRouter()
v1_router.register('orders', OrderViewSet, 'Order')
