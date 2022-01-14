from statistics import mode
from django.shortcuts import render
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from main import serializers
from main import models
from main.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
import jwt
from django.conf import settings
from rest_framework.parsers import FormParser, MultiPartParser


# Create your views here.

@api_view()
def testapi(request):
    return Response({'Bhushan':'Its Working!'})



class RegisterUser(GenericAPIView):
    
    serializer_class = serializers.RegisterUserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status= status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid()
        
        return Response(serializer.data, status= status.HTTP_200_OK)


class StoreCreateAPIView(ListCreateAPIView):

    permission_classes = [ IsAuthenticated, IsOwner ]
    serializer_class = serializers.StoreCreateSerializer
    queryset = models.Store.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner= self.request.user)

class ProductCreateAPIView(ListCreateAPIView):

    permission_classes = [ IsAuthenticated, IsOwner ]
    serializer_class = serializers.ProductCreateSerializer
    parser_classes = [ MultiPartParser, FormParser ]
    queryset = models.Product.objects.all()

    # def get(self, request, *args, **kwargs):

    #     pass

    # def post(self, request, *args, **kwargs):
    #     serialized_data = serializers.ProductCreateSerializer(data = request.data)
    #     if serialized_data.is_valid():
    #         serialized_data.save()
    #         return Response(serialized_data.data, status= status.HTTP_201_CREATED)
    #     return Response(serialized_data.errors)



    def perform_create(self,serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter(owner= self.request.user)