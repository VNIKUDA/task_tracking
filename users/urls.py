from django.urls import path
from users import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("account/<int:pk>", views.UserDetailView.as_view(), name="account")
]

app_name = "users"