import json, requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import models
from zikime.models import Device, Regist, Serial

serial = None

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

    # POST요청이면 form 데이터를 처리한다.
    if request.method == 'POST':
        response = requests.request("GET", "http://www.zikime.com:9999/regist/"+serial)
        json_msg = response.json()
        regist_number = json_msg['regist_number']
        data = request.POST['device_title']

        return JsonResponse({'data:': regist_number == int(data)})

    return render(
        request,
        'zikime/manage.html',
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