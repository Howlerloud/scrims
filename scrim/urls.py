from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.LfpView.as_view(), name='home'),
    path('post-lfp/', views.CreateLfpView.as_view(), name='post_lfp'),
    path('accounts/', include('allauth.urls')),
    path('create_team/', views.CreateTeamView.as_view(), name='create_team'),
    path('lfp/<slug:slug>/', views.LfpDetailView.as_view(), name='lfg_detail'),
    path('lfp/<slug:slug>/delete/', views.LfpDeleteView.as_view(), name='delete_lfp'),
    path('lfp/<slug:slug>/join/', views.join_slot, name='join_slot'),
    path('lfp/<slug:slug>/leave/', views.leave_slot, name='leave_slot'),
]

# path('admin/', admin.site.urls),

