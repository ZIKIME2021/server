from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db.models import fields
from . import models # 👈 해당 model이 존재하는 파일을 import



# class AuthorAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(models.CustomUser, ModelAdmin)

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('date_joined',)
    list_display = ('username', 'email', 'date_joined' )
    fields = ('username', 'email', 'date_joined',)
    search_fields = ['username',]

@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_filter = ('latest_updated_at',)
    list_display = ('device', 'ONF', 'mode', 'IP', 'latitude', 'longitude', 'altitude')
    fieldsets = (
        (None, {
            'fields':('device', 'IP')
        }),
        ('Status',{
            'fields':('ONF', 'mode')
        }),
        ('GPS', {
            'fields':('latitude', 'longitude', 'altitude')
        }),
    )
    search_fields = ['mode','ONF',]
    
@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('serial', 'camera_module_info', 'gps_module_info')
    fieldsets = (
        (None, {
            "fields": ('serial', ),
        }),
        ('Module', {
            'fields':('camera_module_info', 'gps_module_info')
        }),
    )
    

@admin.register(models.Serial)
class SerialAdmin(admin.ModelAdmin):
    list_filter = ('created_at','deleted_at')
    list_display = ('serial_number', 'created_at', 'deleted_at' )
    fieldsets = (
        (None, {
            "fields": (
                'serial_number',
            ),
        }),
    )
    search_fields = ['serial_number',]

@admin.register(models.Regist)
class RegistAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'changed_at')
    list_display = ('device', 'user', 'role', 'created_at', 'changed_at')
    fieldsets = (
        (None, {
            "fields": (
                'device',
            )
        }),
        ('Connecting',{
            'fields':(
                'user', 'role'
            )
        }),
    )
    search_fields = [ 'role',]
    

@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_filter = ('created_at',)
    list_display = ('device', 'master', 'saved_path', 'created_at')
    fieldsets = (
        (None, {
            "fields": (
                'device', 'master'
            ),
        }),
        ('Data', {
            'fields': (
                 'saved_path',
            )
        }),
    )
    
@admin.register(models.StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
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
    