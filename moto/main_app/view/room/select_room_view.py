from django.shortcuts import redirect, render
from main_app.models import Raum
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="login")
def select_room_view(request):
    sorted_rooms = Raum.objects.all().order_by('raum_nr')
    tup_list_raum = []
    for i in range(0, len(sorted_rooms), 2):
        if i + 1 < len(sorted_rooms):
            room1 = sorted_rooms[i]
            room2 = sorted_rooms[i + 1]
            tup = Tup(room1,room2)
            tup_list_raum.append(tup)
    if len(sorted_rooms) % 2 == 1:
        room = sorted_rooms[len(sorted_rooms)-1]
        tup = Tup(room,None)
        tup_list_raum.append(tup)
    return render(request, 'select_room/select_room.html', {'raeume':tup_list_raum})

class Tup:
    def __init__(self, room1, room2):
        self.room1 = room1
        self.room2 = room2