from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response


class CustomUserViewset(ModelViewSet):
    lookup_field = "pk"

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return CustomUserSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request' : self.request}
    
class ExpensesViewset(ModelViewSet):
    def get_queryset(self):
        return Expenses.objects.all().order_by('date')
    
    def get_serializer(self, *args, **kwargs):
        return ExpenseSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request' : self.request}
    
class CreditsViewSet(ModelViewSet):
    def get_queryset(self):
        return Credit.objects.all().order_by('date')
    
    def get_serializer(self, *args, **kwargs):
        return CreditSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request' : self.request}

# Create your views here.
