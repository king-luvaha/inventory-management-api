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
        ordering = ['-last updated']