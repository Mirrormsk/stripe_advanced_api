from django.contrib import admin

from items.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "currency"]
    fields = ["name", "description", "price", "currency"]
    search_fields = ["name"]
    ordering = ["-pk"]
