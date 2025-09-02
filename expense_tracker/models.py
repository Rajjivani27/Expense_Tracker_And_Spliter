from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email','username']

    def __str__(self):
        return self.username

# Create your models here.
