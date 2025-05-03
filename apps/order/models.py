from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
import uuid


def generate_order_serial():
    date_part = now().strftime('%Y%m%d')
    short_uuid = str(uuid.uuid4()).split('-')[0]
    return f"{date_part}-{short_uuid}"


class Order(models.Model):
    serial = models.UUIDField(max_length=32, default=generate_order_serial, editable=False)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.serial}"


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    product = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    number_of_product = models.PositiveSmallIntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"Order item {self.pk} for Order {self.order.serial}"
