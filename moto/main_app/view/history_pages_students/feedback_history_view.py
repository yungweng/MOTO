from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Raum_Belegung, Aufenthalt, Nutzer, Schueler, Zeitraum, Feedback
from datetime import datetime

@login_required(redirect_field_name="login")
def feedback_history_view(request, pupil):
    if(Nutzer.objects.filter(id=pupil).exists()):
        nutzer = Nutzer.objects.get(id=pupil)
        if(Schueler.objects.filter(user_id=nutzer).exists()):
            schueler = Schueler.objects.get(user_id=nutzer)
            hist = []
            students_hist = Feedback.objects.filter(schueler_id = schueler, mensa_feedback = False)
            for s_h in students_hist:
                feedback = ""
                if s_h.feedback_wert=="GOOD":
                    feedback = ":)"
                elif s_h.feedback_wert=="MEDIUM":
                    feedback = ":/"
                elif s_h.feedback_wert=="BAD":
                    feedback = ":("
                hist.append(History(date=s_h.tag.strftime("%d.%m.%y"), time=s_h.zeit.strftime("%H:%M"),feedback=feedback))
            hist = sorted(hist, key=custom_sort_key)
            return render(request, 'history_pages/feedback_history.html', {'hist':hist,'nutzer':nutzer,'pupil':pupil})
    return redirect("master_web")

class History:
    def __init__(self, date, time, feedback):
        self.date = date
        self.time = time
        self.feedback = feedback

def custom_sort_key(history):
    now = datetime.now()
    date_time_str = history.date + ' ' + history.time
    history_time = datetime.strptime(date_time_str, "%d.%m.%y %H:%M")
    return abs((history_time - now).total_seconds())