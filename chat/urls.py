
from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('create/', views.room_create, name="create"),
    path('create/<str:user_nickname>', views.dm_create, name="create_dm"),
    path('list/', views.room_list, name="list"),
    path('detail/<int:room_id>/', views.room_detail, name="detail"),
    path('detail/<int:room_id>/dm', views.dm_detail, name="dm_detail"),
    path('detail/<int:room_id>/access_server/', views.access_server, name="access_server"),
    path('detail/<int:room_id>/exit_server/', views.exit_server, name="exit_server"),
    path('detail/messages/write/', views.message_write, name='message_write'),
    path('detail/messages/', views.chat, name='chat'),
    path('detail/messages/<int:room_id>', views.chat, name='chat'),
    path('my_server_list/', views.my_server_list, name='my_server_list'),
    path('<int:room_id>/delete_server/', views.delete_server, name='delete_server'),
]
