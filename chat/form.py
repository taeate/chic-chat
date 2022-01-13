from django import forms

from chat.models import Room, MyServer


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']
