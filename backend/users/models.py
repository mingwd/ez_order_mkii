# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for authentication
    Extends Django's built-in AbstractUser
    """
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Restaurant Owner'),
    ]
    
    type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
    def __str__(self):
        return f"{self.username} ({self.type})"


class Customer(models.Model):
    """
    Customer profile - extends User
    One-to-one relationship with User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    weight = models.IntegerField(null=True, blank=True)  # in kg or lbs
    memo = models.TextField(blank=True, help_text="Dietary goals and special requirements")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        db_table = 'customer'