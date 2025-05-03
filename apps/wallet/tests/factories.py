import random

import factory
from factory import fuzzy, django

from apps.user.tests.factories import UserFactory
from apps.wallet.models import Wallet


def random_mobile():
    numbers = [random.randint(0, 9) for i in range(9)]
    return '09{}'.format(''.join(map(str, numbers)))


class WalletFactory(django.DjangoModelFactory):
    balance = fuzzy.FuzzyInteger(low=300_000, step=300_000)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Wallet
