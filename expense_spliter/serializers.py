from rest_framework import serializers
from .models import *
from expense_tracker.models import *

class FriendRequestPostSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['requester','requested','status']

class FriendRequestMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['requester','requested','status']

class FriendsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friends
        fields = '__all__'