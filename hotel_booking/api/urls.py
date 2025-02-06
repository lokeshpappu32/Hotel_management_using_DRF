from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, BookingViewSet, AdminViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'admin', AdminViewSet, basename='admin')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]