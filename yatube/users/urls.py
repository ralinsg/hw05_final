from . import views
from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView

app_name = "users"


urlpatterns = [
    path("signup/",
         views.SignUp.as_view(),
         name="signup"
         ),
    path("login/",
         LoginView.as_view(
             template_name="users/login.html"),
         name="login"
         ),
    path("logout/",
         LogoutView.as_view(
             template_name="users/logged_out.html"),
         name="logout"
         ),
    path("password_change/",
         PasswordChangeView.as_view(
             template_name="users/password_change_form.html"),
         name="password_change"
         ),
    path("password_change/done/",
         PasswordChangeDoneView.as_view(
             template_name="users/password_change_done.html"),
         name="password_change_done"
         ),
]
