from django.shortcuts import redirect, render
from main_app.models import Raum, Raum_Belegung, Gruppe
from django.contrib.auth.decorators import login_required

# @login_required(login_url="/login")
def choose_room_view(request):  
    sorted_rooms = Raum.objects.all().order_by('raum_nr')
    return render(request, "choose_room/choose_room.html", {"rooms":sorted_rooms,"room_occupancy":Raum_Belegung.objects.all(),"username":request.user.username, "groups":Gruppe.objects.all()})