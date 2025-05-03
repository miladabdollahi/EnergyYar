from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class RoleEnum(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CUSTOMER = 'customer', 'Customer'

    role = models.CharField(
        max_length=10, choices=RoleEnum.choices, default=RoleEnum.CUSTOMER,
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
