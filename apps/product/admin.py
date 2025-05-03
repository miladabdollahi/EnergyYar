from django.contrib import admin

from apps.core.admin import ModelAdminBase
from apps.order.models import OrderItem
from apps.product.models import Product


@admin.register(Product)
class ProductAdmin(ModelAdminBase):
    list_display = ('title', 'price', 'is_active', 'orders')
    list_filter = ('is_active',)
    ordering = ('-created_time',)

    def orders(self, obj):
        return self.get_list_page(OrderItem, 'Orders', product_id=obj.id)
