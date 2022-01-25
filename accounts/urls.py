from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user_list/', views.user_list, name='user_list'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('searching_user/', views.searching_user, name='searching_user'),
]
