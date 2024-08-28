from django.shortcuts import redirect, render
from main_app.models import Raum_Belegung, Raum_Belegung, Personal, AGKategorie
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required

def change_roomdata_view(request):
    device_id = request.COOKIES.get('device_id')
    if(Raum_Belegung.objects.filter(tablet_id=device_id).exists()):
        raum_belegung = Raum_Belegung.objects.get(tablet_id=device_id)
        raum = raum_belegung.raum
        if not (raum_belegung.ag == None):
            ag = raum_belegung.ag
            personal = ag.leiter
            nutzer = personal.nutzer
            gruppenleiter_gruppe = Group.objects.get(name="Gruppenleitung")
            raumbetreuer_gruppe = Group.objects.get(name="Raumbetreuer")
            personallist = Personal.objects.filter(rechte_gruppe=gruppenleiter_gruppe) | Personal.objects.filter(rechte_gruppe=raumbetreuer_gruppe)
            ap_list = raum_belegung.aufsichtspersonen.all()

            if request.method == "POST":
                if 'change_button_user' in request.POST:
                    username = request.POST.get("user")
                    if(User.objects.filter(username=username).exists()):
                        user = User.objects.get(username=username)
                        personal = Personal.objects.get(user=user)
                        old_username = request.POST.get("change_button_user")
                        old_user = User.objects.get(username=old_username)
                        old_personal = Personal.objects.get(user=old_user)                          
                        r_b = Raum_Belegung.objects.get(ag=ag)
                        if is_personal_avaiable(personal):
                            r_b.aufsichtspersonen.add(personal)
                        if(len(ap_list)>1):
                            r_b.aufsichtspersonen.remove(old_personal)
                        r_b.save()
                    elif(username=="delete"):
                        old_username = request.POST.get("change_button_user")
                        old_user = User.objects.get(username=old_username)
                        old_personal = Personal.objects.get(user=old_user)                          
                        r_b = Raum_Belegung.objects.get(ag=ag)
                        if(len(ap_list)>1):
                            r_b.aufsichtspersonen.remove(old_personal)                           
                        r_b.save()
                elif 'add_button_user' in request.POST:
                    username = request.POST.get("user")
                    if(User.objects.filter(username=username).exists()):
                        user = User.objects.get(username=username)
                        personal = Personal.objects.get(user=user)                          
                        r_b = Raum_Belegung.objects.get(ag=ag)
                        if is_personal_avaiable(personal):
                            r_b.aufsichtspersonen.add(personal)
                        r_b.save()
                elif 'change_button_activity' in request.POST:
                    ag_name = request.POST.get("activity")
                    ag.name = ag_name
                    ag.save()
                elif 'change_button_category' in request.POST:
                    category_name = request.POST.get("category_name")
                    if AGKategorie.objects.filter(name=category_name).exists():
                        ag_kategorie = AGKategorie.objects.get(name=category_name)
                        ag.ag_kategorie = ag_kategorie
                        ag.save()
                elif 'change_button_capacity' in request.POST:
                    capacity = request.POST.get("capacity")
                    try:
                        capacity = int(capacity)
                        if(capacity<=raum.kapazitaet):
                            ag.max_anzahl = capacity
                            ag.save()
                    except:
                        pass    # Fehlermeldung ?

            ap_list = raum_belegung.aufsichtspersonen.all()
            aufsichtspersonen = []
            ap_ids = ap_list.values_list('id', flat=True)
            personallist = personallist.exclude(id__in=ap_ids)
            personal_r_b = Personal.objects.filter(raum_belegung__isnull=False).distinct()
            personal_r_b_ids = personal_r_b.values_list('id', flat=True)
            personallist = personallist.exclude(id__in=personal_r_b_ids)
            # r_bs = Raum_Belegung.objects.all()
            # for r_b in r_bs:
            #     r_b_ap_ids = r_b.aufsichtspersonen.values_list('id', flat=True)
            #     personallist = personallist.exclude(id__in=r_b_ap_ids)
            # personallist.exclude(ap_list)
            i = 1
            for ap in ap_list:
                aufsichtspersonen.append(Tup(personal_default=ap.user.username, value=i, vorname=ap.nutzer.vorname, nachname=ap.nutzer.nachname))
                i += 1
            return render(request, "change_roomdata/change_roomdata.html", {"room_name":raum.raum_nr, "nutzer":nutzer, "personallist":personallist, "ag":ag, "ag_kategorien":AGKategorie.objects.all(),"aufsichtspersonen":aufsichtspersonen})
    
    return redirect("master_web")

class Tup:
    def __init__(self, personal_default, value, vorname, nachname):
        self.personal_default = personal_default
        self.value = value
        self.vorname = vorname
        self.nachname = nachname 


def is_personal_avaiable(personal):
    if (Raum_Belegung.objects.filter(aufsichtspersonen=personal).exists()):
        return False
    return True