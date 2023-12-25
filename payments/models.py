from django.db import models

from items.models import Item


NULLABLE = {'null': True, 'blank': True}


class Discount(models.Model):
    percentage = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='процент скидки')

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'


class Tax(models.Model):
    rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='размер')

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'


class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, **NULLABLE)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
