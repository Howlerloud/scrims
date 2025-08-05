from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from .forms import SixteamForm
from .models import Userstat, Sixteam


class UserList(generic.ListView):
    queryset = Userstat.objects.all()
    template_name = "pages/index.html"
    paginate_by = 10


class LfgView(TemplateView):
    template_name = "pages/lfg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get('slug')
        userstat = get_object_or_404(Userstat, slug=slug)

        context['userstat'] = userstat
        return context


@login_required
def user_teams(request):
    teams = Sixteam.objects.filter(creator=request.user)
    return render(request, 'pages/my_teams.html', {'teams': teams})


@login_required
def create_team(request):
    success = None

    if request.method == 'POST':
        form = SixteamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user  
            team.save()
            success = True
            team.creator = request.user
            try:
                team.save()
                success = True
            except IntegrityError:
                success = False
        else:
            success = False
    else:
        form = SixteamForm()

    return render(request, 'pages/create_team.html', {'form': form, 'success': success})


@login_required
def delete_team(request, slug):
    team = get_object_or_404(Sixteam, slug=slug)

    if request.user != team.creator:
        # Forbidden access, but still returns a response
        return HttpResponseForbidden("This is not your team to delete!")

    if request.method == 'POST':
        try:
            team.delete()
            return redirect('/my-teams?deleted=1')
        except Exception:
            return redirect('/my-teams?deleted=0')

    # If it's a GET request, render confirmation page
    return render(request, 'pages/confirm_delete.html', {'team': team})