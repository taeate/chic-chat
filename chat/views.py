from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from chat.form import RoomForm
from chat.models import Room


@login_required(login_url='accounts:login')
def create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.reg_date = timezone.now()
            room.save()
            room_name = room.name
            return redirect('chat:detail', room_name)
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'chat/room_form.html', context)


@login_required(login_url='accounts:login')
def list(request):
    room_list = Room.objects.all().order_by('-id')
    context = {'room_list': room_list}
    return render(request, 'chat/room_list.html', context)


@login_required(login_url='accounts:login')
def detail(request, room_name):
    room = Room.objects.get(name=room_name)
    context = {'room': room}
    return render(request, 'chat/chatting_room.html', context)
