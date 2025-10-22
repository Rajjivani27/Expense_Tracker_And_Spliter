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

class IncomingRequestSerializer(serializers.ModelSerializer):
    requester = serializers.StringRelatedField()
    accepting_person = serializers.StringRelatedField()
    
    class Meta:
        model = IncomingRequests
        fields = ['requester','accepting_person','accepted','rejected']
        

class OutgoingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutgoingRequests
        fields = ['friend_to_be']

class FriendsSerializer(serializers.ModelSerializer):
    # person1 = serializers.StringRelatedField()
    # person2 = serializers.StringRelatedField()
    class Meta:
        model = Friends
        fields = ['id','person1','person2']