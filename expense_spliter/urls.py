from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('friend_request',FriendRequestViewset,basename="friend_request")
router.register('friends',FriendsViewset,basename="friends")

urlpatterns = [
    
] + router.urls