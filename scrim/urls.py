from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.LfpView.as_view(), name='home'),
    path('post-lfp/', views.CreateLfpView.as_view(), name='post_lfp'),
    path('accounts/', include('allauth.urls')),
    path('create_team/', views.CreateTeamView.as_view(), name='create_team'),

]

# path('admin/', admin.site.urls),

