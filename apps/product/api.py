from rest_framework import mixins

from apps.core.viewsets import CoreViewSet
from apps.product.models import Product
from apps.product.serializers import ProductBaseSerializer, ProductListSerializer


class ProductViewSet(mixins.ListModelMixin, CoreViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductBaseSerializer

    serializers = {
        "list": ProductListSerializer,
    }
