from django.contrib import admin

from apps.order.models import Order, OrderItem
from apps.core.admin import ModelAdminBase


@admin.register(Order)
class OrderAdmin(ModelAdminBase):
    list_display = ('created_time', 'modified_time', 'order_items')
    ordering = ('-created_time',)
    date_hierarchy = 'created_time'

    def order_items(self, obj):
        return self.get_list_page(OrderItem, 'Order Items', order_id=obj.id)


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdminBase):
    list_display = ('order_id', 'product_id', 'number_of_product', 'created_time', 'modified_time')
    ordering = ('-created_time',)
    raw_id_fields = ('order', 'product')
    date_hierarchy = 'created_time'

    def order_id(self, obj):
        return self.get_detail_page(Order, obj.order_id)
