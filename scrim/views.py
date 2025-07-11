from django.shortcuts import render
from django.views import generic
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "pages/index.html"
    paginate_by = 6
