from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

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
            messages.success(request, f"{room.name} 채팅방이 생성되었습니다.")
            return redirect('chat:detail', room_id=room.id)
        else: 
            messages.error(request, "이미 존재하는 채팅방 이름입니다.")
    else:
        messages.error(request, "정상적이지 않은 접근입니다.")
        return redirect('chat:list')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='accounts:login')
def dm_create(request,user_nickname):
    otheruser=User.objects.get(nickname=user_nickname)
    code1 = otheruser.nickname
    code2 = request.user.nickname
    code = sorted([code1,code2])
    code = code[0]+code[1]
    room = Room.objects.filter(name=code)
    if room:
        return redirect('chat:dm_detail', room_id=room.first().id)
    room = Room(host=request.user,name=(code1+code2),room_type="dm")
    room.room_type = 'direct'
    room.save()
    room.part_user.add(request.user)
    room.part_user.add(otheruser)
    return redirect('chat:dm_detail',room_id=room.id)

def room_list(request):
    kw = request.GET.get('kw')
    if kw:
        target = Room.objects.prefetch_related(
            Prefetch('part_user', queryset=User.objects.filter(id=request.user.id), to_attr='part_server'))
        rooms = target.filter(name__icontains=kw) | target.filter(name__startswith=kw)
        if not rooms:
            messages.error(request, "검색된 채팅방이 없습니다.")
    else:
        rooms = Room.objects.prefetch_related(
            Prefetch('part_user', queryset=User.objects.filter(id=request.user.id), to_attr='part_server'))
    rooms = rooms.exclude(room_type="direct")
    context = {'rooms': rooms}
    return render(request, 'chat/room_list.html', context)

@login_required(login_url='accounts:login')
def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    room_detail = "집에 보내줘"
    context = {'room': room, 'room_detail': room_detail}
    return render(request, 'chat/room_detail.html', context)

@login_required(login_url='accounts:login')
def dm_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    room_detail = "집에 보내줘"
    context = {'room': room, 'room_detail': room_detail}

    return render(request, 'chat/room_detail.html', context)

@login_required(login_url='accounts:login')
def access_server(request, room_id):
    room = Room.objects.get(id=room_id)
    request.user.part_server.add(room)
    writer = request.user
    body = f"{writer} 님이 등장하셨어요."
    ChatMessage(room=room, writer=writer, nickname=writer.nickname, message=body, m_type = ChatMessage.Message_Type.ENTER).save()
    return redirect('chat:detail', room_id=room_id)


@login_required(login_url='accounts:login')
def exit_server(request, room_id):
    room = Room.objects.get(id=room_id)
    writer = request.user
    body = f"{writer} 님이 나가셨습니다."
    request.user.part_server.remove(room)
    ChatMessage(room=room, writer=writer, nickname=writer.nickname, message=body, m_type = ChatMessage.Message_Type.EXIT).save()
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

@login_required(login_url='accounts:login')
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
    room = Room.objects.get(id=room_id)
    messages.warning(request, f"{room.name} 채팅방이 삭제되었습니다.")
    room.delete()
    return redirect('chat:my_server_list')
