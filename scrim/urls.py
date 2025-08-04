from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.UserList.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('lfg/<slug:slug>', views.LfgView.as_view(), name="lfg_detail"),
    path('create-team/', views.create_team, name='create_team'),
    # path('team/<slug:slug>/', views.team_detail, name='team_detail'), to use for team profile page

    # path('<slug:slug>/', views.post_detail, name='post_detail'),
]

# path('admin/', admin.site.urls),
# path('hello/about/', about_views.about_me, name='about'),
