from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Raum, Raum_Historie, Aufenthalt, Raum_Belegung
from datetime import datetime, timedelta

@login_required(login_url="login")
def room_usage_history_view(request, raum):
    if(Raum.objects.filter(raum_nr=raum).exists):
        raum = Raum.objects.get(raum_nr=raum)
        raum_historien = Raum_Historie.objects.filter(raum=raum)
        list_histories = []
        for raum_historie in raum_historien:
            date = raum_historie.tag.strftime("%d-%m-%y")
            start_time = raum_historie.zeitraum.startzeit.strftime("%H:%M")
            time = start_time + " - " + raum_historie.zeitraum.endzeit.strftime("%H:%M")
            number=0
            alle_schueler_im_raum = Aufenthalt.objects.filter(raum_id=raum)
            auf = Aufenthalt.objects.filter(raum_id=raum,zeitraum__startzeit__gt=raum_historie.zeitraum.startzeit,zeitraum__endzeit__lte=raum_historie.zeitraum.endzeit)
            # for schueler_in_raum in alle_schueler_im_raum:
            #     if raum_historie.zeitraum.startzeit < schueler_in_raum.zeitraum.startzeit:
            #         if schueler_in_raum.zeitraum.endzeit == None or schueler_in_raum.zeitraum.endzeit <= raum_historie.zeitraum.endzeit:
            #             number += 1
            schueler_ids = auf.values_list('schueler_id', flat=True)
            number = len(list(set(schueler_ids)))
            ag_kategorie = raum_historie.ag_kategorie.name

            history = History(date, time, number, start_time, ag_kategorie)
            list_histories.append(history)
        if(Raum_Belegung.objects.filter(raum=raum).exists()):
            r_b = Raum_Belegung.objects.get(raum=raum)
            date = datetime.now().date().strftime("%d-%m-%y")
            start_time =  r_b.zeitraum.startzeit.strftime("%H:%M")
            time = "Start - " + start_time
            kinder_in_raum = Aufenthalt.objects.filter(raum_id = raum, zeitraum__endzeit__isnull=True)      
            number = len(kinder_in_raum)
            ag_kategorie = r_b.ag.ag_kategorie.name
            history = History(date, time, number, start_time, ag_kategorie)
            list_histories.append(history)

        list_histories = sorted(list_histories, key=custom_sort_key)
        return render(request, 'history_pages/room_usage_history.html', {"historien":list_histories,"raum":raum})
    return redirect('master_web')

class History:
    def __init__(self, date, time, number, start_time, kategorie):
        self.date = date
        self.time = time
        self.number = number
        self.start_time = start_time
        self.kategorie = kategorie

def custom_sort_key(history):
    now = datetime.now()
    date_time_str = history.date + ' ' + history.start_time
    history_time = datetime.strptime(date_time_str, "%d-%m-%y %H:%M")
    return abs((history_time - now).total_seconds())
