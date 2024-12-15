from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=125,
                                verbose_name='category')

    def __str__(self):
        return self.category


class Expense(models.Model):
    description = models.CharField(max_length=255,
                                   verbose_name='description')
    amount = models.IntegerField(verbose_name='amount')
    category_id = models.ForeignKey(to=Category,
                                    verbose_name='category_id',
                                    on_delete=models.CASCADE,
                                    blank=True, null=True)
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                verbose_name='user_id')
    createdAt = models.DateField(verbose_name='creation date')

    def __str__(self):
        return self.description
