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

    # storenameis = serializers.CharField(max_length = 68, min_length = 1, read_only=True)


    class Meta:
        model = models.Store
        fields = [
            'storename',
            'address',
            'id'
            # 'storenameis'
        ]
        # fields = '__all__'

    def validate(self, data):
        storename = data['storename']
        if storename != storename.replace(' ',''):
            raise serializers.ValidationError("Storename should have no spaces between them.")
        else:
            return data


class ProductCreateSerializer(serializers.ModelSerializer):

    storeinfo = serializers.SerializerMethodField('getstoreinfo')

    class Meta:
        model = models.Product
        fields = [
            "storeinfo",
            "store",
            "category",
            "productname",
            "description",
            "mrp",
            "saleprice",
            "image",
            "id"
        ]

    def getstoreinfo(self, instance):

        storeinfo = instance.store.id, instance.store.storename, instance.store.address

        return storeinfo


class CartCreateSerializer(serializers.ModelSerializer):

    productinfo = serializers.SerializerMethodField('getproductinfo')

    class Meta:
        model = models.Cart
        fields = [
            "productinfo",
            "product",
            "quantity"
        ]

    def getproductinfo(self, instance):

        productinfo =  instance.product.productname, instance.product.image, instance.product.saleprice

        return productinfo


class OrderCreateSerializer(serializers.ModelSerializer):

    storeinfo = serializers.SerializerMethodField('getstoreinfo')

    class Meta:
        model = models.Order
        fields = [
            "store",
            "product",
            "storeinfo"
        ]

    def getstoreinfo(self, instance):

        storeinfo = instance.store.id, instance.store.storename, instance.store.address

        return storeinfo


