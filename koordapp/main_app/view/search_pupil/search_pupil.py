from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Aufenthalt, Personal, Raum_Belegung, Schueler
from django.db.models import Q

@login_required(login_url="login")
def search_pupil_view(request):
    schueler = Schueler.objects.all()
    len_sa = 0
    for s in schueler:
        if s.angemeldet:
            len_sa = len_sa + 1
    if request.method == 'POST':
        search = request.POST.get('search')
        if 'button_search' in request.POST:
            schueler2 = []
            for schueler1 in schueler:
                name = schueler1.user_id.vorname + " " + schueler1.user_id.nachname
                if(search.lower() in name.lower()):
                    schueler2.append(schueler1)
            schueler = schueler2
    schueler_active = []
    for s in schueler:
        if s.angemeldet:
            schueler_active.append(s)
    schueler_active = sorted(schueler_active, key=lambda schueler: (schueler.user_id.vorname, schueler.user_id.nachname))
    return render(request, "search_pupil/search_pupil.html", {"schueler":schueler, "schueler_active":schueler_active, "len_sa":len_sa, "len_ss":len(schueler_active)})