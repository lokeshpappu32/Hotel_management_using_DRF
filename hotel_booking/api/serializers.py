from rest_framework import serializers
from .models import User, UserProfile, Booking
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('address', 'photo', 'gender')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

    def validate(self, data):
        if data['check_in_date'] > data['check_out_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        return data