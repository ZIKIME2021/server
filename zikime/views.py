import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import models
from zikime.models import Device, Regist, Serial

def index(request):
    return HttpResponse("Hello World!!!!!!!!!")

def is_resistered(request):
    if request.method == 'GET':
        serial = request.GET['serial']
        devices = Device.objects.all()
        result = False
        for device in devices:
            if serial in str(device):
                result = True
        return JsonResponse({'result': result}, status=200)
