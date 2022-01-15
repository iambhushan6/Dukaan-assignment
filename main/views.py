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
from rest_framework.parsers import FormParser, MultiPartParser
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404



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

    def get(self, request, format=None):

        data = models.Store.objects.all()
        serializer = serializers.StoreCreateSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        
        serializer = serializers.StoreCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = self.request.user)
            current_site = get_current_site(request).domain 
            link = str(f"http://{current_site}/store/{serializer.data['storename']}").replace(' ','')
            return_data = {
                'storelink' : link,
                'id': serializer.data['id']
            }

            return Response(return_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCreateAPIView(ListCreateAPIView):

    permission_classes = [ IsAuthenticated, IsOwner ]
    serializer_class = serializers.ProductCreateSerializer
    parser_classes = [ MultiPartParser, FormParser ]
    queryset = models.Product.objects.all()


    def perform_create(self,serializer):
        return serializer.save()

    def get_queryset(self):
        return self.queryset.filter(owner= self.request.user)


class Storelink_dataAPIView(APIView):

    serializer_class = serializers.ProductCreateSerializer

    def get_object(self, storename):
        try:
            return models.Product.objects.get(store__storename= storename)
        except:
            raise Http404

    def get(self, request, storename, format=None):
        serializer = self.serializer_class(self.get_object(storename))
        serialized_data = serializer.data
        return Response(serialized_data, status= status.HTTP_200_OK)



class CartCreateAPIView(ListCreateAPIView):

    permission_classes = [ IsAuthenticated, IsOwner ]
    serializer_class = serializers.CartCreateSerializer
    queryset = models.Cart.objects.all()


    def perform_create(self,serializer):
        return serializer.save(owner= self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner= self.request.user)


class OrderCreateAPIView(ListCreateAPIView):

    permission_classes = [ IsAuthenticated, IsOwner ]
    serializer_class = serializers.OrderCreateSerializer
    queryset = models.Order.objects.all()


    def perform_create(self,serializer):
        return serializer.save(owner= self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner= self.request.user)