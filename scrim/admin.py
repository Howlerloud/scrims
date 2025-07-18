from django.contrib import admin
from .models import Post, Userstat, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


@admin.register(Userstat)
class UserstatAdmin(SummernoteModelAdmin):

    list_display = ('player', 'role', 'created_on','team_status')
    search_fields = ['player', 'role']
    list_filter = ('team_status',)


admin.site.register(Comment)
