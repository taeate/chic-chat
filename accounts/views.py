from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from accounts.form import UserForm
from django.contrib import messages


def accounts(request):
    return render(request, 'accounts_login.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chat:list')
        else:
            return render(request, 'accounts_login.html', {'error': '아이디 혹은 비밀번호가 틀렸습니다.'})
    else:
        return render(request, 'login.html')


def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = UserForm()
    return render(request, 'signup.html', {
        'form': form,
    })
