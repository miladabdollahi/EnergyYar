from django.urls import reverse
from rest_framework.test import APITestCase

from apps.order.tests.factories import OrderItemFactory


class OrderAPITestCase(APITestCase):

    def test_get_order_items(self):
        order_item = OrderItemFactory()

        url = reverse('v1:Order-get-order-items')
        response = self.client.get(url, kwargs=dict(pk=order_item.order_id))

        self.assertEqual(response.status_code, 200)
