import random

import factory
from factory import django

from apps.user.models import User


def random_mobile():
    numbers = [random.randint(0, 9) for i in range(9)]
    return '09{}'.format(''.join(map(str, numbers)))


class UserFactory(django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    mobile = factory.LazyFunction(random_mobile)
    email = factory.Faker('email')

    class Meta:
        model = User
