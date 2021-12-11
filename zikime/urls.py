from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/', views.is_resistered, name='get'),
    path('lookfor/', views.lookfor, name='lookfor'),
    path('search/', views.search, name='search'),
    path('manage/',views.manage, name='manage'),
    path('mypage/', views.mypage, name='mypage'),
    path('signup/', views.signup, name='signup'),
    path('detail/', views.detail, name='detail'),
    path('detail_area/', views.detail_area, name='detail_area'),
    path('login/',views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]

