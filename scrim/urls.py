from . import views
from django.urls import path, include



urlpatterns = [
    path('', views.UserList.as_view(), name='home'),
    path("accounts/", include("allauth.urls")),
    path('find/', views.FindView.as_view(), name='find'),
    path("lfg/<slug:team_slug>/", views.LfgView.as_view(), name="lfg"),
    # path('<slug:slug>/', views.post_detail, name='post_detail'),
]

# path('admin/', admin.site.urls),
# path('hello/about/', about_views.about_me, name='about'),
