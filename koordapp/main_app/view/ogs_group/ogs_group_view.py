from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Personal, Raum, Gruppe, Schueler
from django.contrib.auth.models import User

@login_required(redirect_field_name="login")
def ogs_group_view(request):

    user = request.user
    search = ''
    if(Personal.objects.filter(user=user).exists()):
        personal = Personal.objects.get(user=user)
        gruppe = None
        if(Gruppe.objects.filter(gruppen_leiter=personal).exists()):
            gruppe = Gruppe.objects.filter(gruppen_leiter=personal)[0]
            if not gruppe.vertreter == None:
                gruppe = None
        if(Gruppe.objects.filter(vertreter=personal).exists()):
            gruppe = Gruppe.objects.get(vertreter=personal) 
        if not gruppe == None:
            schueler = Schueler.objects.filter(gruppen_id=gruppe)
            if request.method == 'POST':
                search = request.POST.get('search')
                if 'button_search' in request.POST:
                    schueler2 = []
                    for schueler1 in schueler:
                        name = schueler1.user_id.vorname + " " + schueler1.user_id.nachname
                        if(search.lower() in name.lower()):
                            schueler2.append(schueler1)
                    schueler = schueler2
        else:
            #fehler Nachricht?
            return redirect("master_web")  
    else:
        #fehler Nachricht?
        return redirect("master_web")
    schueler_active = []
    schueler_passiv = []
    for s in schueler:
        if s.angemeldet:
            schueler_active.append(s)
        else:
            schueler_passiv.append(s)
    schueler_active = sorted(schueler_active, key=lambda schueler: (schueler.user_id.vorname, schueler.user_id.nachname))
    schueler_passiv = sorted(schueler_passiv, key=lambda schueler: (schueler.user_id.vorname, schueler.user_id.nachname))

    return render(request, "ogs_group/ogs_group.html",{"schueler_active":schueler_active, "schueler_passiv":schueler_passiv, "search":search, "group_name":gruppe.name})