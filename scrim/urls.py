from . import views
from django.urls import path, include



urlpatterns = [
    path('', views.UserList.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('lfg/<slug:slug>', views.LfgView.as_view(), name="lfg_detail"),
    # path('<slug:slug>/', views.post_detail, name='post_detail'),
]

# path('admin/', admin.site.urls),
# path('hello/about/', about_views.about_me, name='about'),
