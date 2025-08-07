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
    path('team/<slug:slug>/join/', views.join_team, name='join_team'),
    path('team/<slug:slug>/leave/', views.leave_team, name='leave_team'),

]

# path('admin/', admin.site.urls),

