from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, FormView

from user.forms import RegistrationForm
from user.models import User


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "user/user.html")


class UserRegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'user/registration.html'
    success_url = reverse_lazy('user:user_login')


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('user:detail')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user/user.html'
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        return self.queryset.get(pk=self.request.user.pk)


class LogoutView(View):

    @staticmethod
    def get(request):
        logout(request)
        return render(request, template_name="user/login.html", context={
            "message": "Logged out."
        })
