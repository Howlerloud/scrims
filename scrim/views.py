from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Userstat, Sixteam
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .forms import SixteamForm


class UserList(generic.ListView):
    queryset = Userstat.objects.all()
    template_name = "pages/index.html"
    paginate_by = 10


class LfgView(TemplateView):
    template_name = "pages/lfg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use the correct kwarg name and model field
        slug = self.kwargs.get('slug')
        userstat = get_object_or_404(Userstat, slug=slug)

        context['userstat'] = userstat
        return context


@login_required
def create_team(request):
    success = None

    if request.method == 'POST':
        form = SixteamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user  # 👈 THIS IS CRUCIAL
            team.save()
            success = True
        else:
            success = False
    else:
        form = SixteamForm()

    return render(request, 'pages/create_team.html', {'form': form, 'success': success})