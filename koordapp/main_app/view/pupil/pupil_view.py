from django.shortcuts import redirect, render
from main_app.models import Schueler, Nutzer, Aufenthalt, Raum_Belegung, Gruppe, Personal
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="login")
def pupil_view(request, pupil):
    user = request.user
    if Nutzer.objects.filter(id=pupil).exists():
        nutzer = Nutzer.objects.get(id=pupil)
        if Schueler.objects.filter(user_id=nutzer).exists():
            schueler = Schueler.objects.get(user_id=nutzer)
            gruppe = schueler.gruppen_id
            if(Personal.objects.filter(user=user).exists()):
                personal = Personal.objects.get(user=user)
                aufenthalt = None
                if(Aufenthalt.objects.filter(schueler_id=schueler).exists()):
                            aufenthalte = Aufenthalt.objects.filter(schueler_id=schueler)
                            if(aufenthalte.filter(zeitraum__endzeit=None).exists()):
                                aufenthalt = aufenthalte.get(zeitraum__endzeit=None)
                # if(personal in gruppe.gruppen_leiter.all()):
                aufenthalt = "Abgemeldet"
                aktuelle_ag = "Keine"
                if schueler.angemeldet == True:
                    aufenthalt = "Nicht bekannt"
                    if(schueler.wc == True):
                        aufenthalt = "Toilette"
                    if(schueler.schulhof == True):
                        aufenthalt = "Schulhof"
                    if(Aufenthalt.objects.filter(schueler_id=schueler, zeitraum__endzeit__isnull = True).exists()):
                        aufenthalt = Aufenthalt.objects.get(schueler_id=schueler, zeitraum__endzeit__isnull = True)
                        raum = aufenthalt.raum_id
                        aufenthalt = "Raum " + raum.raum_nr
                        if(Raum_Belegung.objects.filter(raum=raum).exists):
                            r_b = Raum_Belegung.objects.get(raum=raum)
                            if not (r_b.ag==None):
                                aktuelle_ag = r_b.ag.name
                klassen = []
                for schueler1 in Schueler.objects.all():
                    if not (schueler1.klasse in klassen):
                        klassen.append(schueler1.klasse)
                ogs_groups = Gruppe.objects.all()
                
                if request.method == "POST":
                    if 'change_button_ogs_group' in request.POST:
                        ogs_group = request.POST.get('ogs_group')
                        if(Gruppe.objects.filter(name=ogs_group).exists()):
                            ogs_group = Gruppe.objects.get(name=ogs_group)
                            schueler.gruppen_id = ogs_group
                            schueler.save()
                            return redirect("/pupil/"+str(pupil))
                    elif 'change_button_name_eb' in request.POST:
                        name_eb = request.POST.get('name_eb')
                        if not(name_eb==''):
                            schueler.name_eb = name_eb
                            schueler.save()
                    elif 'change_button_kontakt_eb' in request.POST:
                        kontakt_eb = request.POST.get('kontakt_eb')
                        if not(kontakt_eb==''):
                            schueler.kontakt_eb = kontakt_eb
                            schueler.save()
                    elif 'change_button_klasse' in request.POST:
                        klasse = request.POST.get('klasse')
                        if(klasse in klassen):
                            schueler.klasse = klasse
                            schueler.save()
                    elif 'change_button_bus_kind' in request.POST:
                        bus_kind = request.POST.get('bus_kind')
                        if(bus_kind=='1'):
                            schueler.bus_kind=True
                        elif(bus_kind=='2'):
                            schueler.bus_kind=False
                        schueler.save()

                if schueler.bus_kind == True:
                    bus_kind = 'Ja'
                else:
                    bus_kind = 'Nein'

                is_personal_gruppenleiter  = False
                gruppen_leiter = gruppe.gruppen_leiter.all()[0]
                gruppen_raum = gruppe.raum
                if(Raum_Belegung.objects.filter(raum=gruppen_raum).exists()):
                    r_b = Raum_Belegung.objects.get(raum=gruppen_raum)
                    gruppen_leiter = r_b.ag.leiter
                if not gruppe == None:
                    if(personal in gruppe.gruppen_leiter.all() and gruppe.vertreter == None):
                        is_personal_gruppenleiter = True
                    elif gruppe.vertreter == personal:
                        is_personal_gruppenleiter = True

                return render(request, "pupil/pupil.html", {"schueler":schueler, "nutzer":nutzer, "bus_kind":bus_kind, "aufenthalt":aufenthalt, "aktuelle_ag":aktuelle_ag, "ogs_groups":ogs_groups, "klassen":klassen, "user":user, "gruppen_leiter":gruppen_leiter, "is_personal_gruppenleiter":is_personal_gruppenleiter})
        
    return redirect("master_web")