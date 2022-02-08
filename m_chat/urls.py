
from django.urls import path

from m_chat import views

app_name = 'm_chat'

urlpatterns = [
    path('', views.m_room_list, name='m_list'),
    path('chat/list/', views.m_room_list, name='m_list'),
]
