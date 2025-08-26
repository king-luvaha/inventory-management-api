from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InventoryItem, Category, InventoryChange

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class InventoryItemSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'quantity', 'price', 
            'category', 'category_id', 'created_by',
            'date_added', 'last_updated'
        ]
        read_only_fields = ['date_added', 'last_updated']

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return value
    
class InventoryChangeSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = InventoryChange
        fields = '__all__'