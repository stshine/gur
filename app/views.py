import os
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from app.services import ForgejoService
from app.forms import RegisterForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            forgejo_service = ForgejoService(
                os.environ.get("FORGEJO_APIKEY", ""),
                os.environ.get("FORGEJO_URL", "http://localhost:3000")
            )
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            git_user = forgejo_service.create_user(username, email, password)
            if not git_user:
                form.add_error(None, "Failed to register user with Forgejo.")
                return render(request, "registration/register.html", {"form": form})

            form.save()
            return redirect("/accounts/login")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})
