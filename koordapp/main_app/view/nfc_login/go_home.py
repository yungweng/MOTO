from django.shortcuts import redirect, render
from main_app.models import Nutzer, Feedback, Schueler
from datetime import datetime
from main_app.view.home.home_view import home_view

def go_home_view(request, feedback=None):
    tag_id = request.session.get('tag_id', None)
    last_tag_id = request.session.get('last_tag_id', None)
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        return home_view(request, tag_id)
    if not tag_id == None:
        if(Nutzer.objects.filter(tag_id=tag_id).exists()):
            nutzer = Nutzer.objects.get(tag_id=tag_id)
            request.session['last_tag_id'] = tag_id
            request.session['tag_id'] = None
            return render(request, 'go_home/go_home.html', {"nutzer":nutzer})
    elif not last_tag_id == None:
        if not feedback == None:
            if(Nutzer.objects.filter(tag_id=last_tag_id).exists()):
                nutzer = Nutzer.objects.get(tag_id=last_tag_id)
                try:
                    feedback = Feedback.Feedbacks[feedback.upper()].value
                except KeyError:
                    return redirect("home")
                if(Schueler.objects.filter(user_id=nutzer).exists()):
                    schueler = Schueler.objects.get(user_id=nutzer)
                    feedback = Feedback.objects.create(feedback_wert = feedback, schueler_id = schueler, tag = datetime.now().date(), zeit=datetime.now().time())
                    request.session['last_tag_id'] = None
                    redirect("home")
    return redirect("home")