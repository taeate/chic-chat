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
            return redirect('chat:detail', room_id=room.id)
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'chat/room_form.html', context)


@login_required(login_url='accounts:login')
def room_list(request):
    rooms = Room.objects.all().order_by('-id')
    my_servers = Room.objects.prefetch_related(
        Prefetch('part_user', queryset=User.objects.filter(id=request.user.id), to_attr='part_server'))
    context = {'rooms': rooms, 'my_servers': my_servers}
    return render(request, 'chat/room_list.html', context)


@login_required(login_url='accounts:login')
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
    room = Room.object.get(id=room_id)
    request.user.part_server.remove(room)
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
    list(ChatMessage.objects.filter(room=room).values())
    return JsonResponse({
        'message': "성공",
        'resultCode': "S-1",
    })


def chat(request, room_id):
    id = request.GET.get('from_id')
    room = Room.objects.get(id=room_id)
    chats = list(ChatMessage.objects.filter(id__gt=id, room=room).order_by('id').values())

    return JsonResponse({
        'resultCode': "S-1",
        'chats': chats,
    })
