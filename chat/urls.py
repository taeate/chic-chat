from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('create/', views.room_create, name="create"),
    path('list/', views._list, name="list"),
    path('detail/<int:room_id>/', views.room_detail, name="detail"),
    path('detail/<int:room_id>/accessServer/', views.accessServer, name="accessServer"),
    path('detail/messages/write', views.message_write, name='message_write'),
    path('detail/messages/<int:room_id>', views.chat, name='chat'),
]