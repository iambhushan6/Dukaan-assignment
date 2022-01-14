from re import I
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from main import models
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site




User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=60, min_length=6, write_only=True)

    class Meta:
        model = models.User
        fields = ['phone', 'password', 'username', 'id']

    def validate(self, attrs):
        phone = attrs.get('phone','')
        username = attrs.get('username','')
        id = attrs.get('id','')
        _id = attrs.get('_id','')

        return attrs 

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):


    phone = serializers.CharField()
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    authToken = serializers.CharField(max_length = 68, min_length = 6, read_only=True)


    class Meta:
        model = models.User
        fields = ['phone', 'password', 'authToken']

    def validate(self, attrs):
        phone = attrs.get('phone','')
        password = attrs.get('password','')
        user = auth.authenticate( phone= phone, password= password)

        if not user:
            raise AuthenticationFailed("Invalid Credentials")

        return {  
            "phone": user.phone,
            # "username": user.username,
            'authToken': user.tokens
        }
        return super().validate(attrs)


class StoreCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Store
        fields = [
            'storename',
            'address',
        ]

    def validate(self, attrs,request):

        storename = attrs.get('storename','')

        currentlink = get_current_site(request=request).domain
        storelink = 'http://'+currentlink + storename
        return { 
            # 'id': user.id,  
            'storelink': storelink
        }