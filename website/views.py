from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from account.forms import AccountCreationForm


class SignUpView(CreateView):
    form_class = AccountCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'