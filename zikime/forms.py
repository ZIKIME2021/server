from django import forms
from django.forms.widgets import TextInput
from . import models

class UserForm(forms.Form):
    username = forms.CharField(max_length=30, label_suffix='', widget=TextInput(attrs={'size':80}), required=True)
    email = forms.EmailField(label_suffix='', widget=TextInput(attrs={'size':80}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"size":80}),label_suffix='', required=True)    
    repassword = forms.CharField( widget=forms.PasswordInput(attrs={"size":80}),label_suffix='', required=True)
    
    #TODO: username 중복 검사
    def clean_username(self):
        username = self.cleaned_data.get("username") # 필드의 입력값 가져오기
        try:
            models.CustomUser.objects.get(username=username) # 필드의 email값이 DB에 존재하는지 확인
            raise forms.ValidationError("User already exists with that username")
        except models.CustomUser.DoesNotExist:
            return username  # 존재하지 않는다면, 데이터를 반환
        
    
    #TODO: email 중복 검사
    def clean_email(self):
        email = self.cleaned_data.get("email") 
        try:
            models.CustomUser.objects.get(email=email)
            raise forms.ValidationError("User already exists with that email")
        except models.CustomUser.DoesNotExist:
            return email  
        
    #TODO: password 일치 검사
    def clean_repassword(self):
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword") 
        if password != repassword:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password
        
    # save 매서드로 DB에 저장
    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = models.CustomUser.objects.create_user(username, email, password)
        user.save()   
        