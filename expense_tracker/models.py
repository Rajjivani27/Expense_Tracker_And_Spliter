from django.db import models
from django.db.models.signals import (
    post_save,
    post_delete
)
from django.dispatch import receiver
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
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="bank_account")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Online Money"

class CashExpenseTracker(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="cash_account")
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Cash Money"

class Expenses(models.Model):
    expense_choises = [
        ("rent","RENT"),
        ("shopping","SHOPPING"),
        ("food","FOOD"),
        ("snacks","SNACKS"),
        ("travel","TRAVEL"),
        ("cab","CAB(Rapido,Uber,etc.)"),
        ("recharge","REACHARGE"),
        ("grocery","GROCERY"),
        ("dairy_item","DAIRY"),
        ("vegetables","VEGES"),
        ("other","OTHER"),
        ("miscellaneous","MSCL")
    ]

    payment_choices = [
        ("online","ONLINE"),
        ("cash","CASH"),
    ]

    amount = models.IntegerField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="expenses")
    expense_type = models.CharField(choices=expense_choises,default="miscellaneous")
    payment_type = models.CharField(choices=payment_choices,default="cash")
    date = models.DateField()
    note = models.TextField()

class Credit(models.Model):
    payment_choices = [
        ("online","ONLINE"),
        ("cash","CASH"),
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="account_credits")
    amount = models.IntegerField()
    payment_type = models.CharField(choices=payment_choices,default="online")
    date = models.DateField()
    note = models.TextField()


@receiver([post_save],sender = Expenses)
def update_account(sender,instance,created,*args,**kwargs):
    if instance.payment_type is "online":
        try:
            user = instance.user
            online_account = OnlineExpenseTracker.objects.get(user = user)
            online_account.amount = online_account.amount - instance.amount
            online_account.save()
        except Exception as E:
            raise E
    else:
        try:
            user = instance.user
            cash_account = CashExpenseTracker.objects.get(user = user)
            cash_account.amount = cash_account.amount - instance.amount
            cash_account.save()
        except Exception as E:
            raise E
        
@receiver([post_save],sender=Credit)
def update_account_for_credit(sender,instance,created,*args,**kwargs):
    if instance.payment_type is "online":
        try:
            user = instance.user
            online_account = OnlineExpenseTracker.objects.get(user = user)
            online_account.amount = online_account.amount + instance.amount
            online_account.save()
        except Exception as E:
            raise E
    else:
        try:
            user = instance.user
            cash_account = CashExpenseTracker.objects.get(user = user)
            cash_account.amount = cash_account.amount + instance.amount
            cash_account.save()
        except Exception as E:
            raise E

# Create your models here.
