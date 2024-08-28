from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import logout


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")