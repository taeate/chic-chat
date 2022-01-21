from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('create/', views.room_create, name="create"),
    path('list/', views.room_list, name="list"),
    path('detail/<int:room_id>/', views.room_detail, name="detail"),
    path('detail/<int:room_id>/access_server/', views.access_server, name="access_server"),
    path('detail/<int:room_id>/exit_server/', views.exit_server, name="exit_server"),
    path('detail/messages/write/', views.message_write, name='message_write'),
    path('detail/messages/', views.chat, name='chat'),
    path('detail/messages/<int:room_id>', views.chat, name='chat'),
    path('my_server_list/', views.my_server_list, name='my_server_list'),
    path('<int:room_id>/delete_server/', views.delete_server, name='delete_server'),
    path('<int:room_id>/input_room_password/', views.input_room_password, name='input_room_password'),
]
