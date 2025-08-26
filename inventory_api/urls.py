from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import (UserViewSet, CategoryViewSet, InventoryItemViewSet, InventoryChangeViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'inventory', InventoryItemViewSet, basename='inventory')
router.register(r'changes', InventoryChangeViewSet, basename='changes')

urlpatterns = [
    path('', include(router.urls))
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
