from django.shortcuts import redirect, render
from main_app.models import Nutzer
from main_app.view.home.home_view import home_view

def checked_out_view(request):
    tag_id = request.session.get('tag_id', None)
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        return home_view(request, tag_id)
    if not tag_id == None:
        if(Nutzer.objects.filter(tag_id=tag_id).exists()):
            nutzer = Nutzer.objects.get(tag_id=tag_id)
            request.session['tag_id'] = None
            return render(request, 'checked_out/checked_out.html', {"nutzer":nutzer})
    return redirect("home")
            