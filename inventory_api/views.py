from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, Category, InventoryChange, User
from .serializers import (
    InventoryItemSerializer,
    CategorySerializer,
    InventoryChangeSerializer,
    UserSerializer
)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions required for this view.
        """
        if self.action == 'create': # Registration
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Users can only see their own profile (except during registration)
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return User.objects.all()       # Admin can see all users
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()
    
    def perform_create(self, serializer):
        """
        Create user and set user_id in environment for testing
        """
        user = serializer.save()
        return user

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'quantity']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'quantity', 'price', 'last_updated']

    def get_queryset(self):
        user = self.request.user
        queryset = InventoryItem.objects.filter(created_by=user)

        # Filter for low stock items
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None:
            try:
                threshold = int(low_stock)
                queryset = queryset.filter(quantity__lt=threshold)
            except ValueError:
                pass

        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price is not None:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        if max_price is not None:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        return (
            super()
            .get_queryset()
            .select_related("category", "created_by")  # avoid N+1 queries
        )

    def perform_create(self, serializer):
        item = serializer.save(created_by=self.request.user)
        InventoryChange.objects.create(
            item=item,
            user=self.request.user,
            action='CREATE',
            new_quantity=item.quantity,
            notes='Item created'
        )

    def perform_update(self, serializer):
        old_item = self.get_object()
        old_quantity = old_item.quantity

        item = serializer.save()
        new_quantity = item.quantity

        if old_quantity != new_quantity:
            quantity_change = new_quantity - old_quantity
            action_type = 'ADD' if quantity_change > 0 else 'REMOVE'

            InventoryChange.objects.create(
                item=item,
                user=self.request.user,
                action=action_type,
                quantity_change=quantity_change,
                previous_quantity=old_quantity,
                new_quantity=new_quantity,
                notes='Quantity updated'
            )
        else:
            InventoryChange.objects.create(
                item=item,
                user=self.request.user,
                action='UPDATE',
                notes='Details updated'
            )

    def perform_destroy(self, instance):
        InventoryChange.objects.create(
            item=instance,
            user=self.request.user,
            action='DELETE',
            previous_quantity=instance.quantity,
            notes='Item deleted'
        )
        instance.delete()

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        item = self.get_object()
        adjustment = request.data.get('adjustment', None)
        notes = request.data.get('notes', '')

        if adjustment is None:
            return Response(
                {'error': 'Adjustment value is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            adjustment = int(adjustment)
        except ValueError:
            return Response(
                {'error': 'Adjustment must be an integer.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_quantity = item.quantity + adjustment
        if new_quantity < 0:
            return Response(
                {'error': 'Resulting quantity cannot be negative.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_quantity = item.quantity
        item.quantity = new_quantity
        item.save()

        action_type = 'ADD' if adjustment > 0 else 'REMOVE'
        InventoryChange.objects.create(
            item=item,
            user=request.user,
            action=action_type,
            quantity_change=adjustment,
            previous_quantity=old_quantity,
            new_quantity=new_quantity,
            notes=notes
        )

        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        item = self.get_object()
        changes = item.changes.all().order_by('-timestamp')
        serializer = InventoryChangeSerializer(changes, many=True)
        return Response(serializer.data)
    
class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp', 'action']
    ordering = ['-timestamp']

    def get_queryset(self):
        user = self.request.user
        return InventoryChange.objects.filter(user=user)
        