from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User, UserProfile, Booking
from .serializers import UserSerializer, UserProfileSerializer, BookingSerializer
from datetime import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get', 'put'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        user = request.user
        if request.method == 'GET':
            profile, created = UserProfile.objects.get_or_create(user=user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            profile, created = UserProfile.objects.get_or_create(user=user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def booking_count(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        bookings = Booking.objects.filter(user=request.user)
        if start_date:
            bookings = bookings.filter(check_in_date__gte=start_date)
        if end_date:
            bookings = bookings.filter(check_in_date__lte=end_date)
        
        return Response({'total_bookings': bookings.count()})

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Booking.objects.filter(user=user)
        
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(check_in_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(check_in_date__lte=end_date)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdminViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def users_list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def booking_stats(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        bookings = Booking.objects.all()
        if start_date:
            bookings = bookings.filter(check_in_date__gte=start_date)
        if end_date:
            bookings = bookings.filter(check_in_date__lte=end_date)
            
        stats = bookings.values('user__email').annotate(
            total_bookings=Count('id')
        )
        
        return Response(stats)