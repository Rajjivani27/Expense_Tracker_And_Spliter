from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"friends",FriendsViewSet,basename="friends")
router.register(r"friend_requests",FriendRequestsViewSet,basename="friend_requests")

urlpatterns = [
    
] + router.urls