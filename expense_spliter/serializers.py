from rest_framework import serializers
from .models import *
from django.db.models import Q
from expense_tracker.models import *
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework import status

# class SpliterSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Spliter
#         fields = ['user','amount','added_friends']

#     def get_fields(self):
#         fields = super().get_fields()

#         request = self.context['request']

#         queryset = Friends.objects.filter(Q(person1 = request.user) | Q(person2 = request.user))

#         flat_ids = set()

#         for q in queryset:
#             if q.person1.id == request.user:
#                 flat_ids.add(q.person2.id)
#             else:
#                 flat_ids.add(q.person1.id)

#         friends = CustomUser.objects.filter(id__in = flat_ids)

#         fields['added_friends'].queryset = friends

#         return fields



class FriendRequestSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ['accepting_person','accepted','rejected','time']
        read_only_fields = ['requester']

    def validate(self, attrs):
        data = super().validate(attrs)
        request = self.context['request']

        if data['accepting_person'] == request.user:
            raise serializers.ValidationError("You can't send friend request to your self")
        
        queryset = Friends.objects.filter(Q(person1 = request.user,person2 = data['accepting_person']) | Q(person1 = data['accepting_person'],person2 = request.user))

        if queryset:
            raise serializers.ValidationError("You can not send friend request to user who is already your friend")
        
        return data
        

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