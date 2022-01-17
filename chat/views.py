from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from chat.form import RoomForm
from chat.models import *


@login_required(login_url='accounts:login')
def room_create(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.reg_date = timezone.now()
            room.save()
            return redirect('chat:detail', room_id=room.id)
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'chat/room_form.html', context)


@login_required(login_url='accounts:login')
def _list(request):
    room_list = Room.objects.all().order_by('-id')
    my_servers = MyServer.objects.filter(user=request.user)
    context = {'room_list': room_list, 'my_servers': my_servers}
    return render(request, 'chat/room_list.html', context)


@login_required(login_url='accounts:login')
def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    context = {'room': room}
    return render(request, 'chat/chatting_room.html', context)


@login_required(login_url='accounts:login')
def accessServer(request, room_id):
    room = Room.objects.get(id=room_id)
    user = request.user
    MyServer(room=room, user=user).save
    return redirect('chat:detail', room_id=room_id)


def message_write(request: HttpRequest):
    writer = request.POST.get("writer", "")
    body = request.POST.get("body", "")
    room_id = request.POST.get("room_id")
    room = Room.objects.get(id=room_id)
    if not writer:
        raise ValidationError("writer가 없습니다.")

    if not body:
        raise ValidationError("body가 없습니다.")

    ChatMessage(room=room, writer=writer, message=body).save()

    return JsonResponse({
        'message': "성공",
        'resultCode': "S-1"
    })


def chat(request: HttpRequest):
    id = request.GET.get('from_id')
    chats = list(ChatMessage.objects.filter(id__gt=id).order_by('id').values())
    return JsonResponse({
        'resultCode': "S-1",
        'chats': chats,
    })
