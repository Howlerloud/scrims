from django.contrib import admin
from .models import Sixteam
from .models import Userstat
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Sixteam)
class SixteamAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_on', 'slug')
    search_fields = ('name', 'creator__username')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Userstat)
class UserstatAdmin(SummernoteModelAdmin):

    list_display = ('player', 'role', 'created_on','team_status')
    search_fields = ['player', 'role']
    list_filter = ('team_status',)



