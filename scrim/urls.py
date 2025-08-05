from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.UserList.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('lfg/<slug:slug>', views.LfgView.as_view(), name="lfg_detail"),
    path('create-team/', views.create_team, name='create_team'),
    path("my-teams/", views.user_teams, name="my_teams"),
    path("team/<slug:slug>/delete/", views.delete_team, name="delete_team"),
    path('lfp/<slug:slug>/delete/', views.delete_lfp, name='delete_lfp'),
    # path('team/<slug:slug>/', views.team_detail, name='team_detail'), to use for team profile page

    # path('<slug:slug>/', views.post_detail, name='post_detail'),
]

# path('admin/', admin.site.urls),
# path('hello/about/', about_views.about_me, name='about'),
