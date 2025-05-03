from rest_framework import routers

from apps.product.api import ProductViewSet

v1_router = routers.DefaultRouter()
v1_router.register('products', ProductViewSet, 'Product')
