from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.generic import DetailView, CreateView
from django.contrib.auth import views as auth_views
from users.forms import RegisterForm, LoginForm

# Create your views here.
class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name = "users/account.html"


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


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get("username")
            # raw_password = form.cleaned_data.get("password1")
            # user = authenticate(username=username, password=raw_password)

            user = form.save()
            login(request, user)

            return redirect("tasks:task-list")
        
    else:
        form = RegisterForm()

    return render(request, "users/register.html", context={"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        username = form.data.get("username")
        password = form.data.get("password")

        user = authenticate(request, username=username, password=password)

        if form.is_valid():
            if user:
                login(request, user)

                return redirect("tasks:task-list")
        
    else:
        form = LoginForm()

    return render(request, "users/login.html", context={"form": form})

def logout_view(request):
    logout(request)

    return redirect("tasks:task-list")