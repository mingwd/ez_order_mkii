# restaurants/admin.py

from django.contrib import admin
from .models import Restaurant, Tag, Item


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Restaurant admin"""
    list_display = ['name', 'user', 'google_place_id', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'google_place_id', 'address']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'description')
        }),
        ('Location', {
            'fields': ('google_place_id', 'latitude', 'longitude', 'address')
        }),
        ('Media', {
            'fields': ('photo',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin"""
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['id']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Menu Item admin"""
    list_display = ['name', 'restaurant', 'price', 'totalcalories', 'created_at']
    list_filter = ['restaurant', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['tags']  # Nice interface for selecting tags
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('restaurant', 'name', 'description', 'price', 'photo')
        }),
        ('Nutrition (grams)', {
            'fields': ('totalprotein', 'totalgreens', 'totalcarb', 'totalfat', 'totalcalories')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )