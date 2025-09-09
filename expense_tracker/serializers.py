from rest_framework import serializers
from django.db import transaction
from .models import *

class OnlineExpenseTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineExpenseTracker
        fields = ['amount']

class CashExpenseTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashExpenseTracker
        fields = ['amount']

class CustomUserSerializer(serializers.ModelSerializer):
    bank_account = OnlineExpenseTrackerSerializer()
    cash_account = CashExpenseTrackerSerializer()
    password2 = serializers.CharField(write_only=True,style={'input_type':'password'})
    class Meta:
        model = CustomUser
        fields = ['id','email','username','name','password','password2','bank_account','cash_account']
        extra_kwargs = {
            'password' : {'write_only':True, 'style':{'input_type':'password'}}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("password1 and password2 are not matching, they must be same.")
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        online_initial_amount = validated_data.pop('bank_account')
        cash_initial_amount = validated_data.pop('cash_account')

        print(f"Type :- {type(online_initial_amount)}")

        validated_data.pop('password2')
        password = validated_data['password']
        validated_data.pop('password')

        user = CustomUser(**validated_data)

        user.set_password(password)
        user.save()

        online = OnlineExpenseTracker(user=user,**online_initial_amount)
        cash = CashExpenseTracker(user=user,**cash_initial_amount)

        return user
    
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['id','amount','user','expense_type','payment_type','date','note']

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ['id','amount','user','payment_type','date','note']
    

    