from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import settings


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)


    def __str__(self):
        return self.username

class MT5Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    server = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username