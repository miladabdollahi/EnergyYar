import factory
from apps.order.models import Order
import uuid


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    serial = factory.LazyFunction(uuid.uuid4)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory()
    number_of_product = factory.Faker('random_int', min=1, max=10)
    price = factory.LazyAttribute(lambda obj: obj.product.price)
