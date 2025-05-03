from django.urls import reverse
from rest_framework.test import APITestCase

from apps.product.tests.factories import ProductFactory


class ProductAPITestCase(APITestCase):

    def test_product_list(self):
        product = ProductFactory()

        url = reverse('v1:Product-list')
        response = self.client.get(url)

        self.assertEqual(url, f'/api/v1/products/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], product.id)
