from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
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
            request.user.part_server.add(room)
            return redirect('chat'
                            ':detail', room_id=room.id)
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'chat/room_form.html', context)


def room_list(request):
    rooms = Room.objects.prefetch_related(
        Prefetch('part_user', queryset=User.objects.filter(id=request.user.id), to_attr='part_server'))
    context = {'rooms': rooms}
    return render(request, 'chat/room_list.html', context)


def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    context = {'room': room}

    return render(request, 'chat/room_detail.html', context)


@login_required(login_url='accounts:login')
def access_server(request, room_id):
    room = Room.objects.get(id=room_id)
    request.user.part_server.add(room)
    return redirect('chat:detail', room_id=room_id)


@login_required(login_url='accounts:login')
def exit_server(request, room_id):
    room = Room.objects.get(id=room_id)
    if room.host == request.user:
        messages.warning(request, "내가 만든 서버는 못 나감")
    else:
        request.user.part_server.remove(room)
    return redirect('chat:list')


@login_required(login_url='accounts:login')
def message_write(request):
    writer = request.user
    body = request.POST.get("body", "")
    room_id = request.POST.get("room_id")
    room = Room.objects.get(id=room_id)

    if not body:
        raise ValidationError("body가 없습니다.")

    ChatMessage(room=room, writer=writer, nickname=writer.nickname, message=body).save()
    list(ChatMessage.objects.filter(room=room).values())
    return JsonResponse({
        'message': "성공",
        'resultCode': "S-1",
    })


def chat(request, room_id):
    id = request.GET.get('from_id')
    room = Room.objects.get(id=room_id)
    chats = list(ChatMessage.objects.select_related('writer').filter(id__gt=id, room=room)
                 .order_by('id').values())
    return JsonResponse({
        'resultCode': "S-1",
        'chats': chats,
        'writer':'none',
    })


@login_required(login_url='accounts:login')
def my_server_list(request):
    rooms = Room.objects.prefetch_related(
        Prefetch('part_user', queryset=User.objects.filter(id=request.user.id), to_attr='part_server'))
    rooms = rooms.filter(host=request.user)
    context = {'rooms': rooms}
    return render(request, 'chat/my_server_list.html', context)


@login_required(login_url='accounts:login')
def delete_server(request, room_id):
    Room.objects.get(id=room_id).delete()
    return redirect('chat:my_server_list')
