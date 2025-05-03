from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(max_length=125, verbose_name=_('Title of Product.'))
    description = models.TextField(verbose_name=_('Description of Product.'))

    price = models.FloatField(verbose_name=_('Price of Product.'))
    is_active = models.BooleanField(default=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
