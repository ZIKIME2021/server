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
    path('signup/', views.signup, name='signup'),
    path('detail/', views.detail),
]
