import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db import models
from zikime.models import CustomUser, Device, Guest
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests

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

# 회원 가입
def signup(request):
    # signup 으로 POST 요청이 왔을 때, 새로운 유저를 만드는 절차를 밟는다.
    if request.method == 'POST':
        # password와 confirm에 입력된 값이 같다면
        if request.POST['password'] == request.POST['re-password']:
            # user 객체를 새로 생성
            user = CustomUser.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
    # signup으로 GET 요청이 왔을 때, 회원가입 화면을 띄워준다.
    return render(request, 'zikime/signup.html')

# 로그인
def login(request):
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)
        
        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'zikime/login.html', {'error' : 'username or password is incorrect.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, 'zikime/login.html')

# 로그 아웃
def logout(request):
    # logout으로 POST 요청이 들어왔을 때, 로그아웃 절차를 밟는다.
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')

    # logout으로 GET 요청이 들어왔을 때, 로그인 화면을 띄워준다.
    return render(request, 'zikime/login.html')

def index(request):
    return render(request, 'zikime/index.html')


def sos_request(request, serial):
    if request.method == 'GET':
        print(serial)
        return JsonResponse({'result': True}, status=200)


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