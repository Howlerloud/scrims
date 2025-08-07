# scrim/forms.py
from django import forms
from .models import Sixteam, Userstat


class SixteamForm(forms.ModelForm):
    class Meta:
        model = Sixteam
        fields = ['name','discord_name']

    def __init__(self, *args, **kwargs):
        super(SixteamForm, self).__init__(*args, **kwargs)


class LFPForm(forms.ModelForm):
    class Meta:
        model = Userstat
        fields = ['six_team', 'rank', 'role']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LFPForm, self).__init__(*args, **kwargs)
        self.fields['six_team'].queryset = Sixteam.objects.filter(creator=user)

