from django.shortcuts import redirect, render
from main_app.models import Raum, Raum_Belegung, Personal, AGKategorie, AG, Zeitraum, Gruppe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from datetime import datetime
from main_app.view.change_roomdata.change_roomdata_view import is_personal_avaiable

# @login_required(login_url="/login")
def create_activity_view(request, raum):
    if(Raum.objects.filter(raum_nr=raum).exists()):
        raum = Raum.objects.get(raum_nr=raum)
        device_id = request.COOKIES.get('device_id')
        if not(Raum_Belegung.objects.filter(tablet_id=device_id).exists()):
            if not(Raum_Belegung.objects.filter(raum=raum).exists()):
                gruppenleiter_gruppe = Group.objects.get(name="Gruppenleitung")
                raumbetreuer_gruppe = Group.objects.get(name="Raumbetreuer")
                personallist = Personal.objects.filter(rechte_gruppe=gruppenleiter_gruppe) | Personal.objects.filter(rechte_gruppe=raumbetreuer_gruppe)
                p_in_form = []
                r_bs = Raum_Belegung.objects.all()
                defaul_user = None
                for r_b in r_bs:
                    ap_ids = r_b.aufsichtspersonen.values_list('id', flat=True)
                    personallist = personallist.exclude(id__in=ap_ids)
                if (Gruppe.objects.filter(raum=raum).exists()):
                    gruppe = Gruppe.objects.get(raum=raum)
                    # defaul_user = gruppe.gruppen_leiter
                default_personal_list = [Tup(personal_default='0', value=0)]
                default_capacity = None
                default_ag_kategorie = None
                default_activity = None
                if request.method == "POST":
                    default_capacity = request.POST["capacity"]
                    default_ag_kategorie = request.POST["ag_kategorie"]
                    default_activity = name_activity = request.POST["activity"]
                    default_personal_list = []
                    i = 0
                    while('aufsichtsperson_'+str(i) in request.POST):
                        aufsichtsperson = request.POST.get('aufsichtsperson_'+str(i))
                        if(Personal.objects.filter(user__username=aufsichtsperson).exists() or aufsichtsperson == "0"):
                            default_personal_list.append(Tup(aufsichtsperson, i))
                            p_in_form.append(aufsichtsperson)                      
                           
                        i += 1
                    a = request.POST.get('submit_through_button',None)

                    if not a == None:                   
                        if(len(default_personal_list)>=1 and not default_personal_list[0].personal_default=="0"):
                            aufsichtspersonen = []
                            for tup in default_personal_list:
                                if not(tup.personal_default == "0"):
                                    username = tup.personal_default
                                    personal = Personal.objects.get(user__username=username)
                                    aufsichtspersonen.append(personal)
                            
                            max_anzahl = request.POST["capacity"]
                            try:
                                max_anzahl = int(max_anzahl)
                                if max_anzahl <= raum.kapazitaet:
                                    name_ag_kategorie = request.POST["ag_kategorie"]
                                    if AGKategorie.objects.filter(name=name_ag_kategorie).exists():
                                        ag_kategorie = AGKategorie.objects.get(name=name_ag_kategorie)
                                        name_activity = request.POST["activity"]
                                        if(len(name_activity.strip(" "))>0):
                                            if(max_anzahl>0):
                                                zeitraum = Zeitraum.objects.create(startzeit=datetime.now().time(), endzeit=None)
                                                
                                                for p in aufsichtspersonen:
                                                    if not is_personal_avaiable(p):
                                                        aufsichtspersonen.remove(p)
                                                if(len(aufsichtspersonen)>=1):
                                                    ag = AG.objects.create(name=name_activity, max_anzahl=max_anzahl,offene_AG=True,leiter=aufsichtspersonen[0],ag_kategorie=ag_kategorie)
                                                    raum_belegung = Raum_Belegung.objects.create(raum=raum, ag=ag, tablet_id=device_id, zeitraum=zeitraum)
                                                    raum_belegung.aufsichtspersonen.add(*aufsichtspersonen)
                                                    raum_belegung.save()
                                                    return redirect("home")  # Weiterleitung bei erfolgreichen erstellen des raumes
                                            else:
                                                messages.error(request, 'Die maximale Kapazität muss größer als Null sein')
                                        else:
                                            messages.error(request, 'Bitte geben Sie einen Namen für die Aktivität an')
                                    else:
                                        # Error message wen kategorie nicht existiert
                                        messages.error(request, 'Bitte wählen Sie eine Kategorie für die Aktivität aus')
                                else:
                                    messages.error(request, 'Die angegebene maximale Anzahl ist größer als die Raumkapazität. Raumkapazität: ' + str(raum.kapazitaet))
                            except ValueError:
                                #error message wenn capazitaet keine Zahl ist!
                                messages.error(request, 'Bitte geben Sie die maximale Anzahl an Teilnehmern an')
                        else:
                            messages.error(request, 'Bitte wählen Sie eine Aufsichtsperson aus')
                    elif ("button_add_personal" in request.POST):
                        last_item = default_personal_list[-1]
                        if not(last_item.personal_default=='0'):
                            default_personal_list.append(Tup(personal_default='0', value=(last_item.value + 1)))
                    elif ("button_remove_personal" in request.POST):
                        if(len(default_personal_list)>1):
                            last_item = default_personal_list.pop(-1)
                return render(request, "create_activity/create_activity.html", {"room":raum, "personallist":personallist, "ag_kategorien":AGKategorie.objects.all(),"default_personal_list":default_personal_list,"default_capacity":default_capacity,"default_ag_kategorie":default_ag_kategorie,"default_activity":default_activity,"p_in_form":p_in_form})
                
            else:
                pass

    return redirect("master_tablet")

class Tup:
    def __init__(self, personal_default, value):
        self.personal_default = personal_default
        self.value = value