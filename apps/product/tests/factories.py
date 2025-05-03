import factory

from apps.product.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker('word')
    description = factory.Faker('sentence')
    price = factory.Faker('pyfloat', left_digits=2, right_digits=2, positive=True)
    is_active = True
