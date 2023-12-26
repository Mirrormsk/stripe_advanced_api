from django.db import models

from items.models import Item

NULLABLE = {'null': True, 'blank': True}


class Discount(models.Model):
    percent_off = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='процент скидки', default=0)
    amount_off = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='сумма скидки', default=0)
    currency = models.CharField(max_length=3, **NULLABLE, verbose_name='валюта')

    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'

    def __str__(self):
        return (f'{self.amount_off if self.amount_off else ''} '
                f'{self.currency if self.currency else ''}'
                f'{str(self.percent_off) + '%' if self.percent_off else ""}')


class Tax(models.Model):
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='размер')
    display_name = models.CharField(max_length=20, verbose_name='название')
    inclusive = models.BooleanField(verbose_name='включен')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'


class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    discounts = models.ManyToManyField(Discount)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
