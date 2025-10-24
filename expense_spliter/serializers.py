from rest_framework import serializers
from .models import *
from django.db.models import Q
from expense_tracker.models import *
from django.db.models.query import QuerySet

class SpliterSerializer(serializers.ModelSerializer):
    added_friends = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = CustomUser.objects.none()
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Spliter
        fields = ['user','amount','added_friends']

class FriendRequestSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['accepting_person','accepted','rejected','time']
        read_only_fields = ['requester']
        

    def get_fields(self):
        fields = super().get_fields()

        request = self.context['request']
        user = request.user
        obj = self.instance

        # print(f"Requester : {obj.requester}")
        # print(f"Accepting Person:{obj.accepting_person}")

        if obj and not isinstance(obj, QuerySet):
            if user != obj.accepting_person:
                fields['accepted'].read_only = True
                fields['rejected'].read_only = True

        if request.method == 'POST':
            fields['accepted'].read_only = True
            fields['rejected'].read_only = True

        return fields
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)

        request = self.context['request']

        #print(data)

        if data and request.method == 'GET':
            id2 = data['accepting_person']

            accepting_person = CustomUser.objects.get(id=id2)

            data['accepting_person'] = accepting_person.username
        return data

class FriendsSerializer(serializers.ModelSerializer):
    # person1 = serializers.StringRelatedField()
    # person2 = serializers.StringRelatedField()
    class Meta:
        model = Friends
        fields = ['id','person1','person2']

    def to_representation(self, instance):
        data =  super().to_representation(instance) 

        request = self.context['request']

        if data and request.method == 'GET':
            id1 = data['person1']
            id2 = data['person2']

            user1 = CustomUser.objects.get(id=id1)
            user2 = CustomUser.objects.get(id=id2)

            data['person1'] = user1.username
            data['person2'] = user2.username
        return data