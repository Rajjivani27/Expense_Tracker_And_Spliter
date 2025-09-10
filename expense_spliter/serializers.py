from rest_framework import serializers
from .models import *
from expense_tracker.models import *

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['requested','requester']

    def create(self, validated_data):
        fr = FriendRequest(**validated_data)
        fr.save()

        return fr

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = '__all__'