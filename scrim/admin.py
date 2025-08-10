from django.contrib import admin
from .models import CreateTeam, LfpModel


@admin.register(CreateTeam)
class CreateTeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'discord_name', 'created_on', 'rank')
    search_fields = ('team_name', 'creator__username')
    prepopulated_fields = {'slug': ('team_name',)}


@admin.register(LfpModel)
class LfpModelAdmin(admin.ModelAdmin):
    list_display = ('host', 'team', 'get_team_name')

    def get_team_name(self, obj):
        return obj.team.team_name
    get_team_name.short_description = 'Team Name'
