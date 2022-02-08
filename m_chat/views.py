from django.shortcuts import render

from chat.models import *
from django.db.models import Prefetch

def home(request):
    return render(request, 'm_base/m_layout.html')

def m_room_list(request):
    rooms = Room.objects.prefetch_related(
        Prefetch('part_user', queryset=User.objects.filter(id=request.user.id), to_attr='part_server'))
    context = {'rooms': rooms}
    return render(request, 'chat/js/m_chat_list.html', context)
