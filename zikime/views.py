import json, requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import models
from zikime.models import CustomUser, Device, Regist, Serial

serial = '10000000d2814bc1'

def is_resistered(request):
    global serial
    if request.method == 'GET':
        serial = request.GET['serial']
        devices = Device.objects.all()
        result = False
        for device in devices:
            if serial in str(device):
                result = True
        return JsonResponse({'result': result}, status=200)

def complete(request):
    print(request.GET)
    return HttpResponse('Hi')

def index(request):
    return render(
        request,
        'zikime/index.html',
    )

def lookfor(request):
    return render(
        request,
        'zikime/lookfor.html',
    )
    
def search(request):
    return render(
        request,
        'zikime/search.html',
    )
    
def manage(request):
    regist_list = Regist.objects.all()
    # regist_device_list = Device.objects.filter(seirregist_list.divice)
    # regist_list = Regist.objects.allselect_related('device__serial');
    
    #TODO devi ec 에서 정보 받아오기
    return render(
        request,
        'zikime/manage.html',
        {
            'device_list':regist_list
        }
    )

def mypage(request):
    return render(
        request,
        'zikime/mypage.html',
    )

def signup(request):
    return render(request, 'zikime/signup.html',)
    # https://rueki.tistory.com/42 참고 
    if request.method == 'GET':
        return render(request, 'zikime/signup.html')
    # elif request.method =='POST':
    #     username = request.POST.get('username',None)
    #     password = request.POST.get('password',None)
    #     email = request.POST.get('email', None)
    #     re_password = request.POST.get('re-password',None)

    #     res_data ={}
    #     if not (username and password and re_password):
    #         res_data['error'] = '모든 값을 입력해야 합니다!'
        

    #     elif password != re_password:
    #         res_data['error'] = '비밀번호가 다릅니다!'
    #     else:

    #         user = User(
    #             username=username,
    #             password = make_password(password)

    #         )
    #         user.save()
    #     return render(request, 'zikime/signup.html',res_data)
    
def detail(request):
    return render(
    request,
    'zikime/detail.html',
)

def detail_area(request):
    return render(
    request,
    'zikime/detail_area.html',
)
