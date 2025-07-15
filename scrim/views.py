from django.shortcuts import render
from django.views import generic
from .models import Post
from django.views.generic import TemplateView


class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "pages/index.html"
    paginate_by = 6


class FindView(TemplateView):
    template_name = "pages/find.html"


class LfgView(TemplateView):
    template_name = "pages/lfg.html"
