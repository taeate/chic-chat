from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "nickname"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")


class SearchUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]
