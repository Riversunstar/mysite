import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile
from .forms import LoginForm, RegForm, ChangeNickNameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm


def user_login(request):         
    if request.method == 'POST': 
        login_form = LoginForm(request.POST)
        if login_form.is_valid():                        
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))           
    else:
        login_form = LoginForm()        
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():                        
        user = login_form.cleaned_data['user']
        login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def register(request):
    if request.method == 'POST': 
        reg_form = RegForm(request.POST, request = request)
        if reg_form.is_valid():            
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['register_code']
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def user_logout(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def nickname_change(request):
    if request.method == 'POST': 
        nickname_form = ChangeNickNameForm(request.POST, user = request.user)
        if nickname_form.is_valid():
            user = nickname_form.cleaned_data['user']
            nickname_new = nickname_form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = nickname_new
            profile.save()
        return redirect('user_info')
    else:
        nickname_form = ChangeNickNameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改' 
    context['form'] = nickname_form
    context['return_back_url'] = 'user_info'
    return render(request, 'form.html', context)

def bind_email(request):
    return_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST': 
        bindemail_form = BindEmailForm(request.POST, request = request)
        if bindemail_form.is_valid():
            email = bindemail_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
        return redirect('user_info')
    else:
        bindemail_form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定' 
    context['form'] = bindemail_form
    context['return_back_url'] = 'user_info'
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                '465395385@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def password_change(request):
    if request.method == 'POST': 
        password_form = ChangePasswordForm(request.POST, user = request.user)
        if password_form.is_valid():
            new_password = password_form.cleaned_data['new_password_again']
            request.user.set_password(new_password)
            request.user.save()
            logout(request)
        return redirect('user_info')
    else:
        password_form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改' 
    context['form'] = password_form
    context['return_back_url'] = 'user_info'
    return render(request, 'form.html', context)

def forgot_password(request):
    if request.method == 'POST':
        forgot_form = ForgotPasswordForm(request.POST, request=request)
        if forgot_form.is_valid():
            email = forgot_form.cleaned_data['email']
            new_password = forgot_form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session['forgot_password_code']
        return redirect('user_login')
    else:
        forgot_form = ForgotPasswordForm()
        
    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置' 
    context['form'] = forgot_form   
    context['return_back_url'] = 'login'
    return render(request, 'user/forgot_password.html', context)


