from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_items')
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
    class Meta:
        ordering = ['-last_updated']
        unique_together = ('name', 'category')

class InventoryChange(models.Model):
    ACTION_CHOICES = [
        ('ADD', 'Add Stock'),
        ('REMOVE', 'Remove Stock'),
        ('UPDATE', 'Update Details'),
        ('CREATE', 'Create Item'),
        ('DELETE', 'Delete Item'),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='changes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    quantity_change = models.IntegerField(default=0)
    previous_quantity = models.PositiveIntegerField(null=True, blank=True)
    new_quantity = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_action_display()} - {self.item.name} by {self.user.username if self.user else 'System'}"
    
    class Meta:
        ordering = ['-timestamp']