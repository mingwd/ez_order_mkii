# orders/models.py

from django.db import models
from users.models import Customer
from restaurants.models import Restaurant, Item, Tag


class Order(models.Model):
    """
    Order model - represents a complete order from a customer
    """
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    totalprice = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    ordertime = models.DateTimeField(auto_now_add=True)
    
    # AI recommendation fields
    isrecommended = models.BooleanField(default=False, help_text="Was this AI-recommended?")
    aiexplanation = models.TextField(blank=True, help_text="Claude's recommendation reasoning")
    
    def __str__(self):
        ai_badge = "🤖" if self.isrecommended else ""
        return f"{ai_badge} Order #{self.id} - {self.customer.firstname} @ {self.restaurant.name}"
    
    class Meta:
        db_table = 'order'
        ordering = ['-ordertime']  # Newest first


class OrderItem(models.Model):
    """
    Order item - represents individual items in an order
    Many-to-many relationship between Order and Item
    """
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity}x {self.item.name}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this order item"""
        return self.item.price * self.quantity
    
    class Meta:
        db_table = 'orderitem'


class CustomerPreferenceTag(models.Model):
    """
    Automatically learned customer preferences
    Tracks how many times each tag appears in customer's orders
    """
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='preference_tags'
    )
    tag = models.ForeignKey(
        Tag, 
        on_delete=models.CASCADE
    )
    count = models.IntegerField(default=1, help_text="How many times this tag appeared in orders")
    
    def __str__(self):
        return f"{self.customer.firstname} - {self.tag.name} ({self.count}x)"
    
    class Meta:
        db_table = 'customerpreferencetag'
        unique_together = ('customer', 'tag')  # Each customer-tag pair is unique
        ordering = ['-count']  # Most frequent first