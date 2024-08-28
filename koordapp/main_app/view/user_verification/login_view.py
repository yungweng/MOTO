from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.utils import timezone

from main_app.models import Personal

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":  
            form = LoginForm(data=request.POST)
            try:
                if form.is_valid():
                    cleandata=form.cleaned_data
                    #authenticate checks if credentials exists in db
                    user=authenticate(username=cleandata['username'],
                                    password=cleandata['password'])
                    if user is not None:
                        if user.is_active:
                            logout_user_from_all_sessions(user)
                            auth_login(request, user)
                            if(Personal.objects.filter(user=user).exists()):
                                personal = Personal.objects.get(user=user)
                                if(personal.is_password_otp == True):
                                    return redirect("set_new_pw")
                            return redirect("master_web")
                    else:
                        messages.error(request,"Benutzername oder Passwort ist falsch")
                        return redirect("login")
                else:
                    messages.error(request,"Benutzername oder Passwort ist falsch")
            except:
                messages.error(request,"Benutzername oder Passwort ist falsch")
        else:
            form=LoginForm()
            
    else:
        return redirect("master_web")

    back_button = request.session.get("back_button_login", False)
    return render(request, "user_verification/user_login.html", {'form':form, "back_button_login":back_button})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deaktiviere die Fehlermeldungen
        self.error_messages = {}
        self.fields['username'].label = "Benutzername"
        self.fields['password'].label = "Passwort"


def logout_user_from_all_sessions(user):
    # user_sessions = Session.objects.filter(expire_date__gte=timezone.now(), 
    #                                        session_data__contains=user.pk)
    # for s in user_sessions:
    #     req = get_request_from_session(s)
    #     if not req == None:
    #         logout(req)
    # user_sessions.delete()
    # # print("logout user")
    # [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]
    all_sessions  = Session.objects.filter(expire_date__gte=timezone.now())
    for session in Session.objects.all():
        if str(user.pk) == session.get_decoded().get('_auth_user_id'):
            session.delete()

def get_request_from_session(session):
    try:
        return session.get_decoded()['_auth_user_id']
    except Session.DoesNotExist:
        return None