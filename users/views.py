from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import DetailView, CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from users.forms import RegisterForm, LoginForm
from tasks.models import Task

# Create your views here.
class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name = "users/account.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["tasks"] = Task.objects.filter(author=user)

        return context


    def get_object(self, *args):
        username = self.kwargs.get("username")
        user = User.objects.get(username=username)

        return user


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return HttpResponseRedirect(self.success_url)


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = reverse_lazy("tasks:task-list")


class LogoutView(auth_views.LogoutView):
    pass