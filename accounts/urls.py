from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts_login.html'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('add_friend/<int:user_id>/', views.add_friend, name='add_friend'),
    path('searching_user/', views.searching_user, name='searching_user'),
]
