from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import LfpModel, CreateTeam
from .forms import LfpForm, CreateNewTeam


class LfpView(generic.ListView):
    model = LfpModel
    template_name = "pages/index.html"
    context_object_name = 'lfps'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lfp_form'] = LfpForm()  # manually add the form
        return context
    

class CreateLfpView(LoginRequiredMixin, CreateView):
    model = LfpModel
    form_class = LfpForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)


class CreateTeamView(CreateView):
    model = CreateTeam
    form_class = CreateNewTeam
    template_name = 'pages/create_team.html'
    success_url = reverse_lazy('home')  # Redirect after successful form submission