# scrim/forms.py
from django import forms
from .models import Sixteam


class SixteamForm(forms.ModelForm):
    class Meta:
        model = Sixteam
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(SixteamForm, self).__init__(*args, **kwargs)