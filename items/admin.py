from django.contrib import admin

from items.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    fields = ['name', 'description', 'price']
    search_fields = ['name']
    ordering = ['-pk']

