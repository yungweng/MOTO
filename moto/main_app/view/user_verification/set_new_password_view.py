import string, random
from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.shortcuts import redirect
from django.shortcuts import render
from django import forms

from main_app.models import Nutzer, Personal, Raum, Gruppe, AG, Schueler

@login_required(redirect_field_name='login')
def set_new_password_view(request):
    user = request.user
    otp = True
    if(Personal.objects.filter(user=user).exists()):
        personal = Personal.objects.get(user=user)
        otp = personal.is_password_otp
    if request.method == "POST":        
        passwort1 = request.POST["new_password"]
        passwort2 = request.POST["repeat_new_password"]         
        if(passwort1 == passwort2):
            passwort1 = passwort1.replace(" ", "")
            if(passwort1 == passwort2):
                if(len(str(passwort1))>=5):       # TODO: Passwort requirements  
                    if(otp==False):    
                        old_passwort = request.POST["old_password"] 
                        user2=authenticate(username=user.username,password=old_passwort)
                        if user2 == None:                
                            messages.error(request,"Altes Passwort ist nicht korrekt")
                            return render(request, "user_verification/set_new_pw.html", {"otp":otp})   
                    user.set_password(passwort1)
                    user.save()
                    if(Personal.objects.filter(user=user).exists()):
                        personal = Personal.objects.get(user=user)
                        personal.is_password_otp = False
                        personal.save()
                    login(request, user)
                    return redirect("master_web")  
                else:
                    messages.error(request,"Es wurden nicht alle Passwortbedingungen erfüllt: Die Länge muss größer als 5 Zeichen sein") 
            else:
                messages.error(request,"Die Passwörter dürfen keine Leerzeichen enthalten")
        else:
            messages.error(request,"Die beiden Passwörter stimmen nicht überein")
    else:
        pass    #Wenn kein OTP

    return render(request, "user_verification/set_new_pw.html", {"otp":otp})