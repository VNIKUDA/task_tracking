from django.urls import path
import django.contrib.auth.views as auth_views
from users import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/<int:pk>", views.UserDetailView.as_view(), name="account")
]

app_name = "users"