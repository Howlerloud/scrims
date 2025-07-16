from django.shortcuts import render, get_object_or_404
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


def post_detail(request, slug):
    """
    Display an individual :model:`pages.Post`.

    **Context**

    ``post``
        An instance of :model:`pages.Post`.

    **Template:**

    :template:`pages/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "pages/post_detail.html",
        {"post": post},
    )