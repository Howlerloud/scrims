from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Userstat
from django.views.generic import TemplateView


# class PostList(generic.ListView):
#     queryset = Post.objects.all()
#     template_name = "pages/index.html"
#     paginate_by = 6


class UserList(generic.ListView):
    queryset = Userstat.objects.all()
    template_name = "pages/index.html"
    paginate_by = 10


class FindView(TemplateView):
    template_name = "pages/find.html"


class LfgView(TemplateView):
    template_name = "pages/lfg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_slug = self.kwargs.get('team_slug')

        userstat = get_object_or_404(Userstat, team_slug=team_slug)
        context['userstat'] = userstat

        return context


# def post_detail(request, slug):
#     """
#     Display an individual :model:`pages.Post`.

#     **Context**

#     ``post``
#         An instance of :model:`pages.Post`.

#     **Template:**

#     :template:`pages/post_detail.html`
#     """

#     queryset = Post.objects.filter(status=1)
#     post = get_object_or_404(queryset, slug=slug)

#     return render(
#         request,
#         "pages/post_detail.html",
#         {"post": post},
#     )