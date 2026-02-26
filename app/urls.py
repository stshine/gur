from django.urls import include, path

from . import views
from .webhook import gitapi

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("home", views.home, name="home"),
    path("packages/new", views.package_new, name="package_new"),
    path("package/<str:package_name>", views.package_show, name="package_show"),
    path("accounts/register", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("git/", gitapi.urls)
]
