from django.urls import path
from django.contrib.auth import views as auth_views, login

from . import views
app_name = 'accounts'

urlpatterns = [
    path('', views.accounts),
    path('login/', views.login, name='login'),
]