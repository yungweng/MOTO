from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Personal
from django.contrib.auth.models import User

@login_required(redirect_field_name="login")
def preferences_view(request):
    user = request.user
    personal = Personal.objects.get(user=user)
    if request.method == "POST":
        if 'change_button_username' in request.POST:
            username = request.POST.get("username")
            if not username == '':
                if not User.objects.filter(username=username).exists():
                    user.username = username
                    user.save()
        elif 'change_button_vorname' in request.POST:
            firstname = request.POST.get("firstname")
            if not firstname == '':
                personal.nutzer.vorname = firstname
                personal.nutzer.save()
        elif 'change_button_nachname' in request.POST:
            surname = request.POST.get("surname")
            if not surname == '':
                personal.nutzer.nachname = surname
                personal.nutzer.save()
    return render(request, 'preferences/preferences.html', {"user":user, "nutzer":personal.nutzer})