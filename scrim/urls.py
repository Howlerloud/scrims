from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
]

# path('admin/', admin.site.urls),
# path('hello/about/', about_views.about_me, name='about'),
