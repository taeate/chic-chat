from django import forms

from chat.models import Room


class RoomForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Room
        fields = ['name', 'password']
