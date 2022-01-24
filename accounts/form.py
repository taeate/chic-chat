from django import forms
from accounts.models import User


class UserForm(forms.ModelForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
