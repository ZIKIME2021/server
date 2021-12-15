import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.db import models
from zikime.models import CustomUser, Device, Regist, Serial
from django.contrib import auth

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
    
def manage(request):

    devices = set()
    
    for e in Device.objects.select_related('serial'):
        # select_related ()가 없으면 각각에 대한 데이터베이스 쿼리가 생성됩니다.
    # 각 항목에 대한 관련 블로그를 가져 오기위한 반복 반복.
        devices.add(e)
    # regist_list = Regist.objects.all()
    # regist_device_list = Device.objects.filter(seirregist_list.divice)
    # regist_list = Regist.objects.allselect_related('device__serial');
    # device_list = Regist.objects.select_related('user').all()

    #TODO devi ec 에서 정보 받아오기
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