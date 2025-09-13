from rest_framework import serializers
from .models import *
from django.db.models import Q
from expense_tracker.models import *

class SpliterSerializer(serializers.ModelSerializer):
    added_friends = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = CustomUser.objects.none()
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Spliter
        fields = ['user','amount','added_friends']

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        request = self.context.get("request")
        if request:
            user = CustomUser.objects.get(username="Raj_Jivani")
            queryset = Friends.objects.filter(Q(friend_one=request.user) | Q(friend_two=request.user))
            self.fields['added_friends'].queryset = queryset

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