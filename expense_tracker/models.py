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
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class UserDetails(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="details")
    name = models.CharField(max_length=100)
    initial_bank_amount = models.IntegerField(default=0)
    initial_cash_amount = models.IntegerField(default = 0)
# Create your models here.
