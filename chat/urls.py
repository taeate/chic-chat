from django.urls import path

from chat import views

app_name = 'chat'

urlpatterns = [
    path('create/', views.create, name="create"),
    path('list/', views.list, name="list"),
    path('/detail/<str:room_name>/', views.detail, name="detail"),
    path('/detail/<str:room_name>/accessServer/', views.accessServer, name="accessServer")
]