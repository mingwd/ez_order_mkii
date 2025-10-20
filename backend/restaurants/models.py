# restaurants/models.py

from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    """
    Restaurant model
    Links to User (owner) and contains Google Place ID
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='restaurants'
    )
    name = models.CharField(max_length=200)
    google_place_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='restaurants/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'restaurant'


class Tag(models.Model):
    """
    Predefined tags for categorizing menu items
    58 hardcoded tags across 7 categories (managed in frontend)
    """
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tag'
        ordering = ['name']


class Item(models.Model):
    """
    Menu item model
    All nutrition values in grams
    """
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Nutrition (all in grams, owner-inputted)
    totalprotein = models.IntegerField(default=0, help_text="Protein in grams")
    totalgreens = models.IntegerField(default=0, help_text="Vegetable content in grams")
    totalcarb = models.IntegerField(default=0, help_text="Carbohydrates in grams")
    totalfat = models.IntegerField(default=0, help_text="Fat in grams")
    totalcalories = models.IntegerField(default=0, help_text="Total calories")
    
    # Many-to-many relationship with tags
    tags = models.ManyToManyField(Tag, related_name='items', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"
    
    class Meta:
        db_table = 'item'