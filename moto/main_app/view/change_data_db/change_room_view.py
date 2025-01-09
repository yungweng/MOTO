from django.shortcuts import redirect, render
from main_app.models import Raum
def room_change_view(request, id):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            if Raum.objects.filter(id=id).exists():
                room = Raum.objects.get(id=id)
            else:
                if id == 0:
                    if request.method == "POST":
                        name = request.POST.get('name')
                        building = request.POST.get('building')
                        capazity = request.POST.get('capazity')
                        category = request.POST.get('category')
                        error = ""
                        if not(name and name.strip()) or Raum.objects.filter(raum_nr=name).exists():
                                    error += "Fehler beim Namen\n"
                        if not(building and building.strip()):
                                    error += "Fehler beim Geschoss / Gebäude\n"
                        if not(category and category.strip()):
                                    error += "Fehler beim Namen der Kategorie\n"
                        try:
                            capa = int(capazity)
                        except ValueError:
                            error += "Fehler beim Kapazität\n"
                        if error == "":
                            raum = Raum.objects.create(raum_nr=name, geschoss = building, kapazitaet = capa, kategorie=category)
                            raum.save()
                            return redirect("/choose_data/room/"+str(raum.id))
                        else:
                                print("Error: "+ error)
                    return render(request, 'change_data_db/create_room.html')
                return redirect("choose_data_room")

            if request.method == "POST":
                name = request.POST.get('name')
                building = request.POST.get('building')
                capazity = request.POST.get('capazity')
                category = request.POST.get('category')
                error = ""
                if name and name.strip() and not Raum.objects.filter(raum_nr=name).exists():
                            room.raum_nr = name
                            room.save()
                if building and building.strip():
                            room.geschoss = building
                            room.save()
                if category and category.strip():
                            room.kategorie = category
                            room.save()
                if capazity and capazity.strip():
                    try:
                                capa = int(capazity)
                                room.kapazitaet = capa
                                room.save()
                    except ValueError:
                        print()
                
            return render(request, 'change_data_db/change_room.html',{"room" : room})
        return redirect("master_web")
    return redirect("login")