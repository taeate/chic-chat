from django import forms
from accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "nickname")


class SearchUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]
