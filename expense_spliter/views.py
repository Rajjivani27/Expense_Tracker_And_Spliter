from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

class FriendRequestViewset(ModelViewSet):
    def get_queryset(self):
        return FriendRequest.objects.all()
    
    def get_serializer(self,*args,**kwargs):
        request = self.request

        if request.method == "POST":
            return FriendRequestPostSerializer(*args,context=self.get_serializer_context(),**kwargs)
        else:
            return FriendRequestMainSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'requested':'Your request has been sent successfully'},status=status.HTTP_201_CREATED)

    
class FriendsViewset(ModelViewSet):
    def get_queryset(self):
        return Friends.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return FriendsSerializer(*args,context=self.get_serializer_context,**kwargs)
    
    def get_serializer_context(self):
        return {'request':self.request}

        

# Create your views here.
