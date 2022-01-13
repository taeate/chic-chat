from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', auth_views.LoginView.as_view(template_name='accounts_login.html'), name='accounts'),
    path('chat/', include('chat.urls')),
]
