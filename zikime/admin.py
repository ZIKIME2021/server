from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models import fields
from . import models # 👈 해당 model이 존재하는 파일을 import

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('date_joined',)
    list_display = ('username', 'email', 'date_joined' )
    fields = ('username', 'email', 'password', 'date_joined',)
    search_fields = ['username',]
    
@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('serial', 'master', 'nickname')
    fieldsets = (
        (None, {
            "fields": ('master',),
        }),
        ('device', {
            'fields':('serial', 'nickname')
        }),
    )
    
# @admin.register(models.Attachment)
# class AttachmentAdmin(admin.ModelAdmin):
#     list_filter = ('created_at',)
#     list_display = ('device', 'user', 'saved_path', 'created_at')
#     fieldsets = (
#         (None, {
#             "fields": (
#                 'device', 'user'
#             ),
#         }),
#         ('Data', {
#             'fields': (
#                 'saved_path',
#             )
#         }),
#     )
    
@admin.register(models.Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('device', 'user')

@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    fieldsets = (
        (None, {
            'fields':('user', 'device', 'IP')
        }),
        ('Status',{
            'fields':('ONF', 'mode')
        }),
        ('GPS', {
            'fields':('latitude', 'longitude', 'altitude')
        }),
    )