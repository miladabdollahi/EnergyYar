from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewsets import CoreViewSet
from apps.order.models import Order, OrderItem
from apps.order.serializers import (
    OrderBaseSerializer, OrderCreateSerializer, OrderItemListSerializer
)


class OrderViewSet(mixins.CreateModelMixin, CoreViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderBaseSerializer

    serializers = {
        "create": OrderCreateSerializer,
        "get_order_items": OrderItemListSerializer,
    }

    @action(methods=['GET'], detail=True, url_path='items')
    def get_order_items(self, request, *args, **kwargs):
        items = OrderItem.objects.select_related('order').filter(order_id=kwargs.get('pk'))
        page = self.paginate_queryset(items)
        if page is not None:
            serializer = OrderItemListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderItemListSerializer(items, many=True)
        return Response(serializer.data)
