from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='main/main.html'), name='accounts'),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
]