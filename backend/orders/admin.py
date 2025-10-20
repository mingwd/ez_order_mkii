# orders/admin.py

from django.contrib import admin
from .models import Order, OrderItem, CustomerPreferenceTag


class OrderItemInline(admin.TabularInline):
    """Show order items inline within order"""
    model = OrderItem
    extra = 1
    fields = ['item', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin"""
    list_display = ['id', 'customer', 'restaurant', 'totalprice', 'isrecommended', 'ordertime']
    list_filter = ['isrecommended', 'ordertime', 'restaurant']
    search_fields = ['customer__firstname', 'customer__lastname', 'restaurant__name']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {
            'fields': ('customer', 'restaurant', 'totalprice', 'ordertime')
        }),
        ('AI Recommendation', {
            'fields': ('isrecommended', 'aiexplanation'),
            'classes': ['collapse']  # Collapsible section
        }),
    )
    
    readonly_fields = ['ordertime']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order Item admin"""
    list_display = ['order', 'item', 'quantity', 'subtotal']
    list_filter = ['order__ordertime']
    search_fields = ['item__name', 'order__customer__firstname']


@admin.register(CustomerPreferenceTag)
class CustomerPreferenceTagAdmin(admin.ModelAdmin):
    """Customer Preference Tag admin"""
    list_display = ['customer', 'tag', 'count']
    list_filter = ['tag']
    search_fields = ['customer__firstname', 'customer__lastname', 'tag__name']
    ordering = ['-count']