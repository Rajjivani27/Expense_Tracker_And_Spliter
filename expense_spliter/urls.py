from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"sent_requests",OutgoingRequestViewSet,basename="sent_requests")
router.register(r"received_requests",IncomingRequestsViewSet,basename="received_requests")
router.register(r"friends",FriendsViewSet,basename="friends")

urlpatterns = [
    
] + router.urls