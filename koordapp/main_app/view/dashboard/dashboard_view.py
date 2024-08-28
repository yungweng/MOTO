from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Personal, Gruppe, Schueler, Aufenthalt, Raum_Belegung

@login_required(redirect_field_name="login")
def dashboard_view(request):
    user = request.user
    personal = Personal.objects.get(user=user)

    schuelers_in_room = {}
    schuelers_at_home = {}
    schuelers_in_movement = {}

    try:
        if Gruppe.objects.filter(gruppen_leiter=personal).exists():
            ogs_gruppen = Gruppe.objects.filter(gruppen_leiter=personal)
            ogs_group = ogs_gruppen[0]
        elif Gruppe.objects.filter(vertreter=personal).exists():
            ogs_group = Gruppe.objects.get(vertreter=personal)
        ogs_group_room = ogs_group.raum
        schuelers = Schueler.objects.filter(gruppen_id=ogs_group)
        schuelers_in_room = Aufenthalt.objects.filter(zeitraum__endzeit__isnull=True, schueler_id__in=schuelers, raum_id=ogs_group_room)
        schuelers_at_home = schuelers.filter(angemeldet = False)
        schuelers_in_movement = schuelers.filter(angemeldet=True)
        schuelers_in_movement = schuelers_in_movement.exclude(id__in=schuelers_in_room.values('schueler_id'))
    except:
        ogs_group = None

    

    rooms_group_room = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Gruppenraum")
    rooms_learn = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Lernen")
    rooms_sport = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Sport")
    rooms_pause = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Ruhe")
    rooms_creative = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Kreativ")
    rooms_nature = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Natur")
    rooms_food = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Ernährung")
    rooms_other = Raum_Belegung.objects.filter(ag__ag_kategorie__name="Sonstige")

    return render(request, "dashboard/dashboard.html",
                  {"students_in_room":len(schuelers_in_room),
                   "students_at_home":len(schuelers_at_home),
                   "students_in_movement":len(schuelers_in_movement),
                   "rooms_group":len(rooms_group_room),
                   "rooms_sport":len(rooms_sport),
                   "rooms_learn":len(rooms_learn),
                   "rooms_food":len(rooms_food),
                   "rooms_creative":len(rooms_creative),
                   "rooms_nature":len(rooms_nature),
                   "rooms_break":len(rooms_pause),
                   "rooms_other":len(rooms_other),
                   "ogs_group":ogs_group,
                   })