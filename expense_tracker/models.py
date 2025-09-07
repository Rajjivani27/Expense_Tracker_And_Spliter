from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','name']

    def __str__(self):
        return self.username

class OnlineExpenseTracker(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="bank_account")
    initial_amount = models.IntegerField(default=0)

class CashExpenseTracker(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="cash_account")
    initial_amount = models.IntegerField(default=0)

class Expenses(models.Model):
    expense_choises = [
        ("rent","RENT"),
        ("shopping","SHOPPING"),
        ("food","FOOD"),
        ("snacks","SNACKS"),
        ("travel","TRAVEL"),
        ("recharge","REACHARGE"),
        ("grocery","GROCERY"),
        ("dairy_item","DAIRY"),
        ("vegetables","VEGES"),
        ("miscellaneous","MSCL")
    ]

    payment_choices = [
        ("online","ONLINE"),
        ("cash","CASH"),
        ("card","CARD")
    ]

    amount = models.IntegerField()
    expense_type = models.CharField(choices=expense_choises,default="miscellaneous")
    payment_type = models.CharField(choices=payment_choices,default="cash")
    note = models.TextField()
# Create your models here.
