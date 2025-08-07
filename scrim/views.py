from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import SixteamForm, LFPForm
from .models import Userstat, Sixteam, TeamMembership


class UserList(generic.ListView):
    queryset = Userstat.objects.all()
    template_name = "pages/index.html"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['lfp_form'] = LFPForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')

        form = LFPForm(request.POST, user=request.user)
        if form.is_valid():
            six_team = form.cleaned_data['six_team']

            # Check if this team already has a Userstat post
            if Userstat.objects.filter(six_team=six_team).exists():
                return redirect('/?lfp_error=1')

            userstat = form.save(commit=False)
            userstat.player = request.user
            userstat.save()
            return redirect('/?lfp_success=1')

        return self.get(request, form=form)


class LfgView(TemplateView):
    template_name = "pages/lfg.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        userstat = get_object_or_404(Userstat, slug=slug)
        team = userstat.six_team

        # Check if user is already a member
        user = self.request.user
        is_member = False
        if user.is_authenticated and team:
            is_member = team.memberships.filter(user=user).exists()

        context['userstat'] = userstat
        context['team'] = team
        context['is_member'] = is_member
        context['is_full'] = team.memberships.count() >= 6 if team else False

        return context


@login_required
def delete_lfp(request, slug):
    userstat = get_object_or_404(Userstat, slug=slug)

    if request.user != userstat.player:
        return HttpResponseForbidden("You can't delete this post.")

    if request.method == 'POST':
        userstat.delete()
        return redirect('/?lfp_deleted=1')

    return redirect('/')


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
            success = True
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
        return HttpResponseForbidden("This is not your team to delete!")

    if request.method == 'POST':
        try:
            team.delete()
            return redirect('/my-teams?deleted=1')
        except Exception:
            return redirect('/my-teams?deleted=0')

    # show confirmation page
    return render(request, 'pages/confirm_delete.html', {'team': team})


@login_required
def join_team(request, slug):
    team = get_object_or_404(Sixteam, slug=slug)

    # Prevent the same user joining twice
    if TeamMembership.objects.filter(team=team, user=request.user).exists():
        return redirect(f'/lfg/{slug}?already_joined=1')

    # Block join if team is full
    if team.memberships.count() >= 6:
        return redirect(f'/lfg/{slug}?full=1')

    # Add user to the team
    TeamMembership.objects.create(team=team, user=request.user)
    return redirect(f'/lfg/{slug}?joined=1')


@login_required
def leave_team(request, slug):
    team = get_object_or_404(Sixteam, slug=slug)
    membership = TeamMembership.objects.filter(team=team, user=request.user).first()

    if membership:
        membership.delete()

        # Remove only one Userstat connected to this team (if exists)
        userstat = Userstat.objects.filter(player=request.user, six_team=team).first()
        if userstat:
            userstat.six_team = None
            userstat.team_name = "teamless!"
            userstat.save()

        return redirect(f'/lfg/{slug}?left=1')

    return redirect(f'/lfg/{slug}?not_member=1')