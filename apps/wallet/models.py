from django.db import models
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    balance = models.BigIntegerField(default=0)

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="wallets")

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class WalletTransaction(models.Model):
    class TypeChoice(models.TextChoices):
        DEPOSIT = ('deposit', _("Deposit"))
        WITHDRAW = ('withdraw', _("Withdraw"))

    amount = models.IntegerField()
    type = models.CharField(max_length=32, choices=TypeChoice, default=TypeChoice.DEPOSIT)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
