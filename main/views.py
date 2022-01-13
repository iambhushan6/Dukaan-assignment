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