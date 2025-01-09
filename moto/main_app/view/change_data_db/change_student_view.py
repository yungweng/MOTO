from django.shortcuts import redirect, render
from main_app.models import Schueler, Gruppe, Nutzer
def student_change_view(request, id):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:

            klassen = []
            for schueler1 in Schueler.objects.all():
                if not (schueler1.klasse in klassen):
                    klassen.append(schueler1.klasse)

            if Schueler.objects.filter(id=id).exists():
                student = Schueler.objects.get(id=id)
            else:
                if id == 0:
                    if request.method == "POST":
                        ogs_group = request.POST.get('ogs_group')
                        firstname = request.POST.get('firstname')
                        lastname = request.POST.get('lastname')
                        name_eb = request.POST.get('name_eb')
                        kontakt_eb = request.POST.get('kontakt_eb')
                        klasse = request.POST.get('klasse')
                        buskind = request.POST.get('bus_kind')
                        tag_id = request.POST.get('tag_id')
                        error = ""
                        if ogs_group and ogs_group.strip() and not ogs_group == "0" and Gruppe.objects.filter(name=ogs_group).exists():
                                    ogs_group = Gruppe.objects.get(name=ogs_group)
                        else:
                                    error += "Fehler bei der OGS-Gruppe\n"
                        if not(firstname and firstname.strip()):
                                    error += "Fehler beim Vornamen\n"
                        if not(lastname and lastname.strip()):
                                    error += "Fehler beim Nachname\n"
                        if not(name_eb and name_eb.strip()):
                                    error += "Fehler beim Namen der Kontaktperson\n"
                        if not(kontakt_eb and kontakt_eb.strip()):
                                    error = "Fehler beim der Kontaktnummer\n"
                        if (buskind=='1'):
                                    bus_kind = True
                        elif (buskind=='2'):
                                    bus_kind = False
                        else:
                                    error = "Fehler bei der Angabe zum Bus\n"
                        b_tag_id = False
                        if(tag_id and tag_id.strip()):
                                    b_tag_id = True
                        if not(klasse in klassen):
                                    error = "Fehler beim der Klasse\n"
                        if error == "":
                            student = None
                            if b_tag_id == True:
                                new_nutzer = Nutzer.objects.create(vorname=firstname,nachname=lastname, tag_id=tag_id)
                                student = Schueler.objects.create(klasse=klasse, bus_kind=bus_kind, name_eb=name_eb, kontakt_eb=kontakt_eb, user_id=new_nutzer,gruppen_id=ogs_group)
                                student.save()
                            else:
                                new_nutzer = Nutzer.objects.create(vorname=firstname,nachname=lastname)
                                student = Schueler.objects.create(klasse=klasse, bus_kind=bus_kind, name_eb=name_eb, kontakt_eb=kontakt_eb, user_id=new_nutzer,gruppen_id=ogs_group)
                                student.save()
                            return redirect("/choose_data/student/"+str(student.id))
                        else:
                                print("Error: "+ error)
                    return render(request, 'change_data_db/create_student.html',{"ogs_groups":Gruppe.objects.all(),"klassen":klassen})
                return redirect("choose_data_student")

            if request.method == "POST":
                ogs_group = request.POST.get('ogs_group')
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                name_eb = request.POST.get('name_eb')
                kontakt_eb = request.POST.get('kontakt_eb')
                klasse = request.POST.get('klasse')
                buskind = request.POST.get('bus_kind')
                tag_id = request.POST.get('tag_id')
                if(ogs_group and ogs_group.strip() and not ogs_group == "0" and Gruppe.objects.filter(name=ogs_group).exists()):
                            ogs_group = Gruppe.objects.get(name=ogs_group)
                            student.gruppen_id = ogs_group
                            student.save()
                if(firstname and firstname.strip()):
                            student.user_id.vorname = firstname
                            student.user_id.save()
                if(lastname and lastname.strip()):
                            student.user_id.nachname = lastname
                            student.user_id.save()
                if(name_eb and name_eb.strip()):
                            student.name_eb = name_eb
                            student.save()
                if(kontakt_eb and kontakt_eb.strip()):
                            student.kontakt_eb = kontakt_eb
                            student.save()
                if(buskind=='1'):
                            student.bus_kind=True
                            student.save()
                elif(buskind=='2'):
                            student.bus_kind=False
                            student.save()
                if(tag_id and tag_id.strip()):
                            student.user_id.tag_id = tag_id
                            student.user_id.save()
                if(klasse in klassen):
                            student.klasse = klasse
                            student.save()
                            #return redirect("/choose_data/student/"+str(student.id))
            bus_kind = "Nein"
            if student.bus_kind == True:
                bus_kind = "Ja"
            return render(request, 'change_data_db/change_student.html',{"student" : student, "ogs_groups":Gruppe.objects.all(),"klassen":klassen, "bus_kind":bus_kind})
        return redirect("master_web")
    return redirect("login")