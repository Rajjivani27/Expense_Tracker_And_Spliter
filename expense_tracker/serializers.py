from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True,style={'input_type':'password'})
    class Meta:
        model = CustomUser
        fields = ['id','email','username','name','password','password2']
        extra_kwargs = {
            'password' : {'write_only':True, 'style':{'input_type':'password'}}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("password1 and password2 are not matching, they must be same.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data['password']
        validated_data.pop('password')

        user = CustomUser(**validated_data)

        user.set_password(password)
        user.save()

        return user
    

    