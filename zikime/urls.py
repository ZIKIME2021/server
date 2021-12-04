from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get/', views.is_resistered, name='get'),
    path('lookfor/', views.lookfor),
    path('search/', views.search),
    path('manage/',views.manage),
    path('mypage/', views.mypage),
    path('regist/', views.device_regist, name='device_regist'),
    path('signup/', views.signup, name='signup'),
]
