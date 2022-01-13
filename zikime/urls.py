from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('get/', views.is_resistered, name='get'),
    path('lookfor/', views.lookfor, name='lookfor'),
    path('search/', views.search, name='search'),
    path('manage/',views.manage, name='manage'),
    path('mypage/<int:pk>/', views.mypage, name='mypage'),
    path('signup/', views.signup, name='signup'),
    path('manage/detail/add_guest/', views.add_guest, name='add_guest'),
    path('manage/detail/', views.detail, name='detail'),
    path('detail_area/', views.detail_area, name='detail_area'),
    path('manage/<int:pk>/delete/', views.delete_device, name='delete_device'),
    path('login/',views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('sos/<str:serial>/', views.sos_request, name='sos_request'),
    path('detail/delete_guest/<int:fk>', views.delete_guest, name='delete_guest'),
    path('manage/regist_device/', views.regist_device, name='regist_device'),
]

