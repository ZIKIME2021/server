from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from zikime.models import CustomUser

# Create your views here.
# 회원가입
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],
                                            email=request.POST['email'],)
            user.save()
            auth.login(request, user)
            return redirect('zikime/index.html')
        return render(request, 'accounts/signup.html')
    return render(request, 'accounts/signup.html')