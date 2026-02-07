from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("home", views.home, name="home"),
    path("accounts/register", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
