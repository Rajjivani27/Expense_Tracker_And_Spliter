from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('users',CustomUserViewset,basename="users")
router.register('expenses',ExpensesViewset,basename="expenses")
router.register('credit',CreditsViewSet,basename="credit")

urlpatterns = [

]+ router.urls
