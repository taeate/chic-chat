from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
app_name = 'accounts'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='accounts_login.html'), name='accounts'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]