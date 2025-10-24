from django.shortcuts import render
from expense_spliter.models import FriendRequest
from expense_spliter.serializers import FriendRequestSerializer
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class CustomUserViewset(ModelViewSet):
    lookup_field = "pk"

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return CustomUserSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request' : self.request}
    
    @action(detail=True,methods=['get'],permission_classes=[IsAuthenticated])
    def sent_requests(self,request,pk=None):
        user = self.get_object()
        sent_requests = FriendRequest.objects.filter(requester = user)
        serializer = FriendRequestSerializer(sent_requests,context=self.get_serializer_context(),many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=True,methods=['get'],permission_classes = [IsAuthenticated])
    def received_requests(self,request,pk=None):
        user = self.get_object()
        received_requests = FriendRequest.objects.filter(accepting_person = user)
        serializer = FriendRequestSerializer(received_requests,context=self.get_serializer_context(),many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

    
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
