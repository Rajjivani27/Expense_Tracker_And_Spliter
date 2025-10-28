from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed

class SplitShareViewSet(ModelViewSet):
    lookup_field = 'pk'

    def get_permissions(self):
        request = self.request
        user = request.user

        if user.is_staff or user.is_superuser:
            return [AllowAny()]
        
        if request.method in ['destroy','update','partial_update']:
            return [IsUserOrReadOnly()]
        else:
            return [IsAuthenticated()]  
        
    def get_serializer(self, *args, **kwargs):
        return SpliteShareSerializer(*args,context=self.get_serializer_context(),**kwargs)

    def get_serializer_context(self):
        return {'request':self.request}
            

class SpliterViewSet(ModelViewSet):
    lookup_field = 'pk'
    def get_permissions(self):
        request = self.request

        if request.method == 'destroy' or request.method == 'update' or request.method == 'partial_update':
            return [IsAuthorOrReadOnly()]
        elif request.method == 'create':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]
        
    def get_queryset(self):
        return Spliter.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return SpliterSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        friends_data = data.pop("added_friends")
        

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user = request.user)
        

        for fd in friends_data:
            user = CustomUser.objects.get(id = fd['user'])
            share_amount = fd['share_amount']
            SplitShare.objects.create(expense = obj,user = user,share_amount=share_amount)
        return Response(serializer.data,status=status.HTTP_200_OK)


class FriendRequestsViewSet(ModelViewSet):
    lookup_field = 'pk'
    def get_permissions(self):
        request = self.request

        if request.method == 'destroy':
            return [IsAuthorOrReadOnly()]
        elif request.method == 'create' or request.method == 'get':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated()]
        
    def get_queryset(self):
        return FriendRequest.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return FriendRequestSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request' : self.request}
    
    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(requester=request.user)

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()

        if user and ((user != obj.accepting_person) and (not user.is_staff) and (not user.is_superuser)) :
            return Response({'detail':'You do not have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        user = request.user
        obj = self.get_object()

        if user and ((user != obj.accepting_person) and (not user.is_staff) and (not user.is_superuser)) :
            return Response({'detail':'You do not have permission to perform this action'},status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

class FriendsViewSet(ModelViewSet):
    def get_permissions(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return [AllowAny()]
        
        if self.action == SAFE_METHODS:
            return [AllowAny()]
        elif self.action == 'destroy':
            return [IsParticipatingParty()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return Friends.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return FriendsSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request':self.request}

# Create your views here.
