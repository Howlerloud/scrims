# scrim/forms.py
from django import forms
from .models import CreateTeam, LfpModel


class CreateNewTeam(forms.ModelForm):
    class Meta:
        model = CreateTeam
        fields = ['team_name', 'discord_name', 'rank', 'team_logo']


class LfpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Start with no teams by default
        self.fields['team'].queryset = CreateTeam.objects.none()
        if user and user.is_authenticated:
            self.fields['team'].queryset = CreateTeam.objects.filter(owner=user).order_by('team_name')

    class Meta:
        model = LfpModel
        fields = ['team', 'average_rank']
