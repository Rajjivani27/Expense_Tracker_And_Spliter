from rest_framework import serializers
from .models import *
from expense_tracker.models import *

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['requested','requester','status']

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = '__all__'