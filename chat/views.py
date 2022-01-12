from django.shortcuts import render

from chat.models import Room


def create(request):
    return


def list(request):
    room_list = Room.objects.all().order_by('-id')
    context = {'room_list': room_list}
    return render(request, 'chat/room_list.html', context)


def detail(request):
    return
