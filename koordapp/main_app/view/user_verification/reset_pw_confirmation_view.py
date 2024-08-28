from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import logout


def reset_pw_confirmation_view(request):
    return render(request, "user_verification/reset_pw_confirmation.html")