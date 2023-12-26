from django.contrib import admin
from payments.models import Order, Discount, Tax


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    fields = ['items',
              'discounts',
              'tax_rates']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ['amount_off', 'currency', 'percent_off']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['percentage',
                    'display_name',
                    'inclusive']
    fields = ['percentage',
              'display_name',
              'inclusive',
              'description']
    search_fields = ['display_name']

