import factory
from factory import fuzzy, django
from apps.user.tests.factories import UserFactory
from apps.payment.models import Payment, Gateway


class PaymentFactory(django.DjangoModelFactory):
    amount = fuzzy.FuzzyInteger(low=10_000, high=40_000_000, step=300_000)
    issuer_user = factory.SubFactory(UserFactory)
    reason = fuzzy.FuzzyChoice(Payment.ReasonChoice.values)
    status = Payment.ReasonChoice.PENDING.value

    class Meta:
        model = Payment


class GatewayFactory(django.DjangoModelFactory):
    title = fuzzy.FuzzyText()
    mode = fuzzy.FuzzyChoice(choices=Gateway.ModeChoice.values)
    type = fuzzy.FuzzyChoice(choices=Gateway.TypeChoice.values)

    class Meta:
        model = Gateway
