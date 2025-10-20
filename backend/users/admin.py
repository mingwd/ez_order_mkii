# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = ['username', 'email', 'type', 'is_staff', 'date_joined']
    list_filter = ['type', 'is_staff', 'is_superuser']
    
    # Add 'type' field to the User admin form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Type', {'fields': ('type',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('User Type', {'fields': ('type',)}),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Customer admin"""
    list_display = ['firstname', 'lastname', 'user', 'age', 'gender', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['firstname', 'lastname', 'user__username']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'firstname', 'lastname')
        }),
        ('Details', {
            'fields': ('age', 'gender', 'weight', 'memo')
        }),
    )