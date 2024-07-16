from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

# Create your views here.
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

    return render(request, "registration/register.html", context={"form": form})

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

    return render(request, "registration/login.html", context={"form": form})

def logout_view(request):
    logout(request)

    return redirect("tasks:task-list")