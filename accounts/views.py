from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect

from accounts.form import UserForm, SearchUserForm


def accounts(request):
    return render(request, 'accounts_login.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username, password1=password)
        if user:
            auth_login(request, user)
            user.active = True
            return redirect('chat:list')
        else:
            return redirect('accounts:login')


def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            signed_user.active = True
            messages.success(request, "회원가입 환영합니다.")
            return redirect('chat:list')
    else:
        form = UserForm()
    return render(request, 'signup.html', {
        'form': form,
    })


def logout(request):
    request.user.active = 'False'
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


def searching_user(request):
    if request.method == "POST":
        form = SearchUserForm(request.POST)
        if form.is_valid():
            nickname = form.save(commit=False)
            search_user = User.objects.get(nickname=nickname)
            return redirect('chat:list', search_user=search_user)
    return redirect('chat:list')


def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user_list.html', context)


def searching_user(request):
    kw = request.GET.get('kw')
    find_friend = User.objects.get(nickname=kw)
    if kw:
        find_friend = User.objects.filter(nickname__icontains=kw)

    return render(request, 'friend_search.html', {'find_friend': find_friend})
