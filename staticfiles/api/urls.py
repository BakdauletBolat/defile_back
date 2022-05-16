import uuid
from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include


urlpatterns = [
    path('auth/',include('users.urls')),
    path('product/',include('product.urls')),
    path('store/',include('store.urls'))
]
