from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('create/', views.create, name="create"),
    path('list/', views.list, name="list"),
    path('<int:room_id>/', views.detail, name="detail"),
]
