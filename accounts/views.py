from accounts.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpRequest
from django.shortcuts import render, redirect

from accounts.form import UserForm


def accounts(request):
    return render(request, 'accounts_login.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, "회원가입 환영합니다.")
            return redirect('chat:list')
        else:
            messages.success(request, "회원가입 환영합니다.")
            return redirect('accounts:login')


def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            return redirect('chat:list')
    else:
        form = UserForm()
    return render(request, 'signup.html', {
        'form': form,
    })


def logout(request):
    auth_logout(request)
    return redirect('/')
