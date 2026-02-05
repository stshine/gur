from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/register", views.register, name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
]
