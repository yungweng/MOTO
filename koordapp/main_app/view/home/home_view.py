from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from main_app.models import Raum_Belegung, Aufenthalt, Nutzer, Schueler, Zeitraum, Personal, Feedback
from datetime import datetime
from main_app.view.user_verification.login_view import logout_user_from_all_sessions
from django.contrib import messages

def home_view(request, tag_id = None):
    if request.user.is_authenticated:
        logout(request)
    request.session["back_button_login"] = True
    device_id = request.COOKIES.get('device_id')
    if not (Raum_Belegung.objects.filter(tablet_id=device_id).exists()):
        return redirect("choose_room")
    r_b = Raum_Belegung.objects.get(tablet_id=device_id)
    raum = r_b.raum
    if request.method == 'POST':
        if(tag_id == None):
            tag_id = request.POST.get('tag_id')
        request.session['tag_id'] = tag_id
        if(Aufenthalt.objects.filter(raum_id=raum, schueler_id__user_id__tag_id=tag_id, zeitraum__endzeit__isnull=True).exists()):
            return redirect("leave_room")
        else:
            if(Nutzer.objects.filter(tag_id=tag_id).exists()):
                nutzer = Nutzer.objects.get(tag_id=tag_id)
                if(Schueler.objects.filter(user_id=nutzer).exists()):
                    if len(raum.get_schueler_in_raum()) < r_b.ag.max_anzahl:
                        schueler = Schueler.objects.get(user_id=nutzer)
                        if(Aufenthalt.objects.filter(schueler_id=schueler, zeitraum__endzeit__isnull = True).exists()):
                            aufenthalt = Aufenthalt.objects.get(schueler_id=schueler, zeitraum__endzeit__isnull = True)
                            zeitraum = aufenthalt.zeitraum
                            zeitraum.endzeit = datetime.now().time()
                            zeitraum.save()
                        if(schueler.angemeldet == False):
                            schueler.angemeldet = True
                        if(schueler.wc == True):
                            schueler.wc = False
                        if(schueler.schulhof == True):
                            schueler.schulhof = False
                        schueler.save()
                        zeitraum = Zeitraum.objects.create(startzeit = datetime.now().time(), endzeit = None)
                        Aufenthalt.objects.create(raum_id=raum, zeitraum=zeitraum, schueler_id=schueler, tag=datetime.now().date())
                        if "mensa" in raum.raum_nr or "Mensa" in raum.raum_nr:
                            Feedback.objects.create(feedback_wert = Feedback.Feedbacks.GOOD, schueler_id = schueler, tag = datetime.now().date(), zeit=datetime.now().time(), mensa_feedback=True)
                        return redirect('checked_in')
                    else:
                        messages.error(request,"Die maximale Raumkapazität wurde bereits erreicht")
                else:
                    if(Personal.objects.filter(nutzer=nutzer).exists()):
                        p = Personal.objects.get(nutzer=nutzer)
                        logout_user_from_all_sessions(p.user)
                        request.session['was_logged_in'] = True
                        login(request, p.user)
                        return redirect("master_tablet")
    return render(request,"home/home.html", {"room":raum})
