from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField()
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    hotel_name = models.CharField(max_length=255)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    num_persons = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']