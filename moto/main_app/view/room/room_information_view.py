from django.shortcuts import redirect, render
from main_app.models import Raum, Raum_Belegung, Gruppe, Aufenthalt
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="login")
def room_information_view(request, raum):
    if(Raum.objects.filter(raum_nr=raum).exists()):
        raum = Raum.objects.get(raum_nr=raum)
        raum_belegung = 'Keine'
        ogs_group, nutzungstyp, aufsichtsperson, aktuelle_kinderanzahl, is_room_active, r_b = [None, None, None, None, False, None]
        if(Raum_Belegung.objects.filter(raum=raum).exists()):
            is_room_active = True
            r_b = Raum_Belegung.objects.get(raum=raum)
            if not(r_b.ag == None):
                raum_belegung = r_b.ag.name
                nutzungstyp = r_b.ag.ag_kategorie.name
                aufsichtsperson = r_b.ag.leiter.nutzer.vorname + " " + r_b.ag.leiter.nutzer.nachname
            elif not (r_b.gruppe==None):
                gruppe = Gruppe.objects.get(raum=raum)
                ogs_group = gruppe.name
                raum_belegung = "Gruppenraum"
                aufsichtsperson = gruppe.gruppen_leiter.nutzer.vorname + " " + gruppe.gruppen_leiter.nutzer.nachname
        if(Gruppe.objects.filter(raum=raum).exists()):
            gruppe = Gruppe.objects.get(raum=raum)
            ogs_group = gruppe.name
        kinder_in_raum = Aufenthalt.objects.filter(raum_id = raum, zeitraum__endzeit__isnull=True)
        
        aktuelle_kinderanzahl = len(kinder_in_raum)
        #print(raum_belegung)

        return render(request, 'room_information/room_information.html', {"raum":raum,
                                        "aktuelle_kinderanzahl":aktuelle_kinderanzahl,
                                        "aufsichtsperson":aufsichtsperson,
                                        "ogs_gruppe":ogs_group,
                                        "nutzungstyp":nutzungstyp,
                                        "raum_belegung":raum_belegung,
                                        "is_room_active":is_room_active,
                                        "r_b":r_b,
                                        })
    return redirect('master_web')