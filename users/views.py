from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import DetailView, CreateView
from django.contrib.auth import views as auth_views
from users.forms import RegisterForm, LoginForm

# Create your views here.
class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name = "users/account.html"


    def get_object(self, *args):
        username = self.kwargs.get("username")
        user = User.objects.get(username=username)

        return user



class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("tasks:task-list")


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = reverse_lazy("tasks:task-list")


class LogoutView(auth_views.LogoutView):
    pass