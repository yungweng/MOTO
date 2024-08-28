from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Aufenthalt, Raum_Belegung, Nutzer, Schueler, Personal, Raum_Belegung
from datetime import datetime
from main_app.view.remove_tablet.remove_tablet_view import remove_tablet
from main_app.view.home.home_view import home_view

def leave_room_view(request):
    if not request.session.get('tag_id', None) == None:
        tag_id = request.session.get('tag_id', None)
        device_id = request.COOKIES.get('device_id')
        r_b = Raum_Belegung.objects.get(tablet_id=device_id)
        raum = r_b.raum
        if(Aufenthalt.objects.filter(raum_id=raum, schueler_id__user_id__tag_id=tag_id, zeitraum__endzeit__isnull=True).exists()): # ist abgemeldeter Nutzer wirklich im Raum?
            if(Nutzer.objects.filter(tag_id=tag_id)):
                nutzer = Nutzer.objects.get(tag_id = tag_id)
                if request.method == 'POST':
                    # print(tag_id)
                    # return home_view(request, tag_id)
                    if(Schueler.objects.filter(user_id=nutzer).exists()):
                        schueler = Schueler.objects.get(user_id=nutzer)
                        aufenthalt = Aufenthalt.objects.get(raum_id=raum, schueler_id__user_id__tag_id=tag_id, zeitraum__endzeit__isnull=True)
                        zeitraum = aufenthalt.zeitraum
                        zeitraum.endzeit = datetime.now().time()
                        zeitraum.save()
                        if not request.POST.get('tag_id', None) == None:
                            tag_id = request.POST.get('tag_id')
                            return home_view(request, tag_id)
                        if('div_name' in request.POST):
                            s = request.POST.get('div_name')
                            if('leave_school_button' == s):
                                schueler.angemeldet = False
                                schueler.save()
                                return redirect('go_home')                    
                            elif('leave_room_button' == s):   
                                return redirect('checked_out')
                            elif('toilet_button' == s):
                                schueler.wc = True
                                schueler.save() 
                                return redirect('checked_out')
                                # request.session['tag_id'] = None  
                                # return redirect('home')
                            elif('school_yard_button' == s):  
                                schueler.schulhof = True
                                schueler.save()
                                return redirect('checked_out')
                                # request.session['tag_id'] = None
                                # return redirect('home')
                        else:
                            return redirect('checked_out')
                    elif(Personal.objects.filter(user=nutzer).exists()):
                        personal = Personal.objects.get(user=nutzer)
                        if(Raum_Belegung.objects.filter(aufsichtsperson=personal).exists()):
                            r_b = Raum_Belegung.objects.get(aufsichtsperson=personal)
                            return remove_tablet(request, r_b.tablet_id)      
                return render(request, 'leave_room/leave_room.html', {"nutzer":nutzer})
            return redirect("home")
        else:
            return redirect("checked_in")
    return redirect("home")