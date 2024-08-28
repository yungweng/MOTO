from django.shortcuts import redirect, render
from main_app.models import Raum
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="login")
def room_selection_view(request, raum):
    if(Raum.objects.filter(raum_nr=raum).exists()):
        raum = Raum.objects.get(raum_nr=raum)
        return render(request, 'room_selection/room_selection.html', {"raum":raum})
    return redirect('master_web')