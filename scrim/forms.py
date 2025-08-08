# scrim/forms.py
from django import forms
from .models import CreateTeam, LfpModel


class CreateNewTeam(forms.ModelForm):
    class Meta:
        model = CreateTeam
        fields = ['team_name', 'discord_name', 'rank']


class LfpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['team'].queryset = CreateTeam.objects.filter(owner=user)  # Add owner field first

    class Meta:
        model = LfpModel
        fields = ['team', 'average_rank']
