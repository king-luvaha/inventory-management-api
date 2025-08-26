from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, InventoryItem, InventoryChange

# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_per_page = 20

# Inventory Item Admin
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'category', 'created_by', 'date_added', 'last_updated')
    list_filter = ('category', 'created_by', 'date_added')
    search_fields = ('name', 'description')
    readonly_fields = ('date_added', 'last_updated')
    list_per_page = 20

    fieldsets = (
        (None, {'fields': ('name', 'description', 'category', 'created_by')}),
        ('Inventory Details', {'fields': ('quantity', 'price')}),
        ('Timestamps', {'fields': ('date_added', 'last_updated'), 'classes': ('collapse',)}),
    )

# Inventory Change Admin
@admin.register(InventoryChange)
class InventoryChangeAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'action', 'quantity_change', 'previous_quantity', 'new_quantity', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    readonly_fields = ('timestamp')
    search_fields = ('item__name', 'user__username', 'notes')
    list_per_page = 20

    def has_add_permission(self, request):
        # Prevent adding changes manually through admin
        return False