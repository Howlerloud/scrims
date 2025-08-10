from django.views.generic.edit import CreateView
from django.views.generic import DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import LfpModel, CreateTeam, PlayerSlot
from .forms import LfpForm, CreateNewTeam


# Shows all LFP posts, New team posts will be displayed at the top
class LfpView(generic.ListView):
    model = LfpModel
    template_name = "pages/index.html"
    context_object_name = 'lfps'
    paginate_by = 10
    queryset = LfpModel.objects.all().order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lfp_form'] = LfpForm(user=self.request.user)
        return context


# Lets a logged-in user create an LFP post
class CreateLfpView(LoginRequiredMixin, CreateView):
    model = LfpModel
    form_class = LfpForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.host = self.request.user
        messages.success(self.request, f'LFP "{form.instance.team.team_name}" was successfully created.')
        return super().form_valid(form)


# Lets a user delete their own LFP post
class LfpDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LfpModel
    template_name = "pages/confirm_delete.html"
    success_url = reverse_lazy('home')

    def test_func(self):
        # superusers can delete anything; otherwise only the host
        return self.request.user.is_superuser or self.get_object().host == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        team_name = self.object.team.team_name
        messages.success(request, f'LFP for "{team_name}" was successfully deleted.')
        return super().post(request, *args, **kwargs)


# Shows the detail page for a specific LFP
class LfpDetailView(DetailView):
    model = LfpModel
    template_name = "pages/lfg.html"
    context_object_name = "lfp"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lfp = self.get_object()
        context['user_in_team'] = lfp.slots.filter(player=self.request.user).exists()
        return context


# Lets a user create a new team
class CreateTeamView(CreateView):
    model = CreateTeam
    form_class = CreateNewTeam
    template_name = 'pages/create_team.html'
    success_url = reverse_lazy('profile')  # send the user to their profile after creating a new team

    def form_valid(self, form):
        form.instance.owner = self.request.user  # set team owner
        messages.success(self.request, f'Team "{form.instance.team_name}" was successfully created.')
        return super().form_valid(form)


# User joins a free slot in a team
def join_slot(request, slug):
    lfp = get_object_or_404(LfpModel, slug=slug)

    if PlayerSlot.objects.filter(player=request.user, lfp=lfp).exists():
        messages.warning(request, "You're already part of this team.")
        return redirect('lfg_detail', slug=slug)

    empty_slot = PlayerSlot.objects.filter(lfp=lfp, player__isnull=True).first()
    if empty_slot:
        empty_slot.player = request.user
        empty_slot.save()
        messages.success(request, "You joined the team.")
    else:
        messages.error(request, "No slots available.")

    return redirect('lfg_detail', slug=slug)


# User leaves a team they're in
def leave_slot(request, slug):
    lfp = get_object_or_404(LfpModel, slug=slug)
    slot = PlayerSlot.objects.filter(lfp=lfp, player=request.user).first()
    if slot:
        slot.player = None
        slot.save()
        messages.success(request, "You left the team.")
    else:
        messages.error(request, "You are not part of this team.")
    return redirect('lfg_detail', slug=slug)


# Profile page that shows only the teams this user owns
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "pages/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # show only teams created by the user
        ctx['teams'] = CreateTeam.objects.filter(owner=self.request.user).order_by('-created_on')
        return ctx


# Lets a user delete a team they own
class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CreateTeam
    success_url = reverse_lazy('profile')

    # Ensure only the owner can delete, and lookup by slug
    def get_object(self, queryset=None):
        return get_object_or_404(
            CreateTeam.objects.filter(owner=self.request.user),
            slug=self.kwargs['slug']
        )

    def test_func(self):
        return self.get_object().owner == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        team_name = self.object.team_name
        messages.success(request, f'Team {team_name} was successfully deleted.')
        return super().post(request, *args, **kwargs)