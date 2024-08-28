from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main_app.models import Gruppe, Personal, Raum_Belegung

@login_required(redirect_field_name="login")
def representation_view(request):
    user = request.user
    if user.is_superuser:
        if request.method == "POST":
            if "change_button_representation" in request.POST:
                gruppe_name = request.POST.get("change_button_representation")
                neue_vertretung = request.POST.get("representation_"+gruppe_name)
                if Personal.objects.filter(user__username=neue_vertretung).exists():
                    p_neu = Personal.objects.get(user__username=neue_vertretung)
                    if Gruppe.objects.filter(vertreter=p_neu).exists():
                        gruppe = Gruppe.objects.get(vertreter=p_neu)
                        gruppe.vertreter = None
                        gruppe.save()
                    # gruppe_name = request.POST.get("group")
                    if Gruppe.objects.filter(name=gruppe_name).exists():
                        gruppe = Gruppe.objects.get(name=gruppe_name)
                        gruppe.vertreter = p_neu
                        gruppe.save()
        users = Personal.objects.all()
        # raum_belegung_ids = Raum_Belegung.objects.filter(aufsichtspersonen__in=users).values_list('id', flat=True)
        # users = users.exclude(raum_belegung__id__in=raum_belegung_ids)
        groups = Gruppe.objects.all().order_by('name')
        return render(request, 'representation/representation.html', {"groups": groups,"users":users})
    return redirect("master_web")