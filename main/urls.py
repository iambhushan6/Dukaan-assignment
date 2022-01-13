from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.testapi, name='testapi'),


    path('dukaan/login', views.LoginAPIView.as_view(), name='login'),

    path('dukaan/register', views.RegisterUser.as_view(), name='register'),

    path('dukaan/store', views.StoreCreateAPIView.as_view(), name='storecreate')
    
]
