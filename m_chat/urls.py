
from django.urls import path

from m_chat import views

app_name = 'm_chat'

urlpatterns = [
    path('', views.home, name='home')
]
