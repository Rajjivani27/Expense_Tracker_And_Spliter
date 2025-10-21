from django.shortcuts import render
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from django.db.transaction import atomic
from rest_framework import status

class IncomingRequestsViewSet(ModelViewSet):
    lookup_field = "accepting_person"
    def get_queryset(self):
        return IncomingRequests.objects.all()
    
    def get_permissions(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return [AllowAny()]
        
        if self.action == 'destroy':
            return [IsAuthorOrReadOnly()]
        return [IsAuthenticated()]
    
    @action(detail=False,methods=['get'])
    def received_requests(self,request):
        user = request.user
        received_requests = IncomingRequests.objects.all(accepting_person = user)
        serializer = self.get_serializer(received_requests,many=True)
        return Response(serializer.data)
    
    def get_serializer(self, *args, **kwargs):
        return IncomingRequestSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_serializer_context(self):
        return {'request':self.request}
    
class OutgoingRequestViewSet(ModelViewSet):
    lookup_field = "requester"

    def get_permissions(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return [AllowAny()]
        
        if self.action == 'destroy':
            return [IsAuthorOrReadOnly()]
        return [IsAuthenticated()]
    
    @action(detail=False,methods=['get'])
    def sent_requests(self,request):
        user = request.user
        sent_requests = OutgoingRequests.objects.filter(requester=user)
        serializer = self.get_serializer(sent_requests,many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return OutgoingRequests.objects.all()
    
    def get_serializer(self, *args, **kwargs):
        return OutgoingRequestSerializer(*args,context=self.get_serializer_context(),**kwargs)
    
    def get_parser_context(self, http_request):
        return {'request':self.request}
    
    @atomic
    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(requester = request.user)

        accepting_user = data.get('friend_to_be')
        print(f"User : {request.user}")
        
        accepting_person = CustomUser.objects.get(id=accepting_user)
        print(f"Accepting Person : {accepting_person}")

        IncomingRequests.objects.create(
            requester = request.user,
            accepting_person = accepting_person
        )

        return Response(data=serializer.data,status=status.HTTP_201_CREATED)



# Create your views here.
