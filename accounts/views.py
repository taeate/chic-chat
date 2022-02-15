from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect

from accounts.form import UserForm, SearchUserForm, LoginForm
from chat.models import Room


def accounts(request):
    return render(request, 'accounts_login.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            auth_login(request, user)
            user.is_active = 1
            user.save()
            messages.success(request, f"돌아오셨군요ㅠㅠ {user.nickname}님..")
            return redirect('chat:list')
        else:
            messages.warning(request, "잘못된 아이디/비밀번호 입니다.")
            return redirect('accounts:login')
    return render(request, 'accounts_login.html')


def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            signed_user.is_active = 1
            signed_user.save()
            messages.success(request, "회원가입 환영합니다.")
            return redirect('chat:list')
    else:
        form = UserForm()
    return render(request, 'signup.html', {
        'form': form,
    })


def logout(request):
    request.user.is_active = 0
    request.user.save()
    auth_logout(request)
    return redirect('/')


@login_required(login_url='accounts:login')
def add_friend(request, user_id):
    user = User.objects.get(id=user_id)
    if user != request.user:
        request.user.friends.add(user)
    else:
        messages.warning(request, '자기 자신은 친구 추가 하지 않아도 영원한 친구입니다.')
    return redirect('accounts:user_list')



def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'friend_list.html', context)



def user_list_all(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'all_user_list.html', context)



def user_list_online(request):
    users = User.objects.filter(is_active=1)
    context = {'users': users}
    return render(request, 'online_user_list.html', context)


def add_friend_searchpage(request):
    return render(request, 'friend_search.html')


def searching_user(request):
    kw = request.GET.get('kw')
    find_friend = User.objects.filter(nickname__icontains=kw) | User.objects.filter(nickname__startswith=kw)

    return render(request, 'friend_search.html', {'find_friend': find_friend})

