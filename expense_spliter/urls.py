from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"friends",FriendsViewSet,basename="friends")
router.register(r"friend_requests",FriendRequestsViewSet,basename="friend_requests")
router.register(r"spliter",SpliterViewSet,basename="spliter")
router.register(r"split_share",SplitShareViewSet,basename="split_share")

urlpatterns = [
    
] + router.urls