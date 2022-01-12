import json
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db import models
from zikime.forms import UserForm
from zikime.models import CustomUser, Device, Guest
from django.contrib import auth, messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
from django.urls import reverse

def is_resistered(request):
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

def register(request):
    return render(request, 'zikime/register.html')

def index(request):
    return render(
        request,
        'zikime/index.html',
    )

@login_required
def lookfor(request):
    devices = set()
    for e in Device.objects.filter(master=request.user):
        devices.add(e)
        
    # TODO:
    # GUEST로 있는 기기들의 목록도 가져와야함.
    
    return render(
        request,
        'zikime/lookfor.html',
        {
            'device_list':devices
        }
    )
    
    
    
    
def search(request):
    return render(
        request,
        'zikime/search.html',
    )
    

@login_required
def manage(request):

    devices = set()
    
    for e in Device.objects.filter(master=request.user):
        devices.add(e)    

    return render(
        request,
        'zikime/manage.html',
        {
            'device_list':devices
        }
    )


def mypage(request):
    return render(
        request,
        'zikime/mypage.html',
    )



# 선택된 기기에 대한 정보를 GET으로 parameter 보내주기
@csrf_exempt
def detail(request):
    if request.method == 'GET':
        guests = set()
        device_id = request.GET.get('device_id')
        device = Device.objects.get(id=device_id)
        for guest in Guest.objects.filter(device=device_id):
            guests.add(guest)

    context = {
        'device':device,
        'guest_list':guests,
    }

    return render(
    request,
    'zikime/detail.html',
    context,    
    )

def detail_area(request):
    return render(
    request,
    'zikime/detail_area.html',
)

def add_guest(request):

    if request.method == 'POST':
        device_id = request.GET['device_id']
        p = Guest.objects.create(
            user = CustomUser.objects.get(username=request.POST['protector-username']),
            device= Device.objects.get(id=device_id)
        )
        # print(request.POST['protector-email'])
    
    return redirect('/manage/detail/?device_id='+device_id)

def delete_device(request, pk):
    device = get_object_or_404(Device, id=pk)
    device.delete()
    return redirect('/manage')


def signup(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'회원가입 성공! 로그인을 해주세요.', )
            return render(request, 'zikime/login.html')
            return HttpResponseRedirect('/')
        else:
            pass
            messages.error(request,'가입정보를 다시 입력해주세요.')
    else:
        messages.success(request,'get')
        
    return render(request, 'zikime/signup.html', {'form':form,})

# 로그인
def login(request): 
    parameter = dict()
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        if username == '' or password=='':
            return render(request, 'zikime/login.html')
            
        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)
        
        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            messages.success(request,'로그인 성공! 환영합니다.')
            return redirect('/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            messages.error(request,'로그인 실패! 로그인 정보가 일치하지 않습니다. ')
            parameter['username'] = username
        
    return render(request, 'zikime/login.html', parameter)



# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        messages.warning(request,'로그아웃 하셨습니다. 안녕히가십시오.')
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, 'zikime/login.html')

def index(request):
    return render(request, 'zikime/index.html')


def sos_request(request, serial):
    if request.method == 'GET':
        device_id = request.GET['device_id']
        email_list = set()
        for guest in Guest.objects.filter(device = device_id):
            email_list.add(CustomUser.objects.get(username=guest)['email'])


def history_save(request):
    if request.method == 'POST':
        return


def delete_guest(request, fk):
    next = request.GET['next']
    user = Guest.objects.filter(user=fk)
    user.delete()
    return redirect('/manage/detail/?device_id='+next)


def regist_device(request):
    regist_num = request.GET['device-number']
    URL = "http://www.zikime.com:9999/device-management/register/" + regist_num
    print(URL)
    response = requests.get(URL)
    res_json = response.json()

    if res_json['registered']:
        Device.objects.create(
            master = request.user,
            serial = res_json['serial'],
        )
    else:
        # alert incorrect regist_number
        pass
    return redirect('/manage')


# NOT COMPLETE
def sos_api(request):
    if request.method == 'GET':
        device_id = request.GET['device_id']
        email_list = set()
        for guest in Guest.objects.filter(device = device_id):
            email_list.add(CustomUser.objects.get(username=guest)['email'])