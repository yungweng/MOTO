from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from main_app.models import Nutzer, Personal, Schueler
from itertools import chain

@login_required(redirect_field_name="login")
def set_nfc_set_view(request):
    tag_id = request.session.get('tag_id', None)
    b = False
    if not request.POST.get('tag_id', None) == None:
        tag_id = request.POST.get('tag_id')
        request.session['tag_id'] = tag_id
        b = True
    if not tag_id == None:
        schueler = Schueler.objects.all()
        s_users = [s.user_id for s in schueler]
        p_users = []
        if request.user.is_superuser:
            personal = Personal.objects.all()
            p_users = [p.nutzer for p in personal]
        tag_username = "Niemand"
        nutzer = None
        if(Nutzer.objects.filter(tag_id=tag_id).exists()):
            nutzer = Nutzer.objects.get(tag_id=tag_id)
            tag_username = nutzer.vorname + " " + nutzer.nachname
        if request.method == 'POST' and b == False:
            search = request.POST.get('search')
            if 'button_search' in request.POST:
                s_users2 = []
                for user in s_users:
                    name = user.vorname + " " + user.nachname
                    if(search.lower() in name.lower()):
                        s_users2.append(user)
                s_users = s_users2
                p_users2 = []
                for user in p_users:
                    name = user.vorname + " " + user.nachname
                    if(search.lower() in name.lower()):
                        p_users2.append(user)
                p_users = p_users2
            if 'button_change_tag' in request.POST:
                new_tag_owner_id = request.POST.get('button_change_tag')
                if not nutzer == None:
                    nutzer.tag_id = None
                    nutzer.save()
                    request.session['tag_id'] = None
                if Nutzer.objects.filter(id=new_tag_owner_id).exists():
                    new_nutzer = Nutzer.objects.get(id=new_tag_owner_id)
                    tag_username = new_nutzer.vorname + " " + new_nutzer.nachname
                    new_nutzer.tag_id = tag_id
                    new_nutzer.save()
                    request.session['tag_id'] = None
                else:
                    return redirect(request.path)
        s_users = sorted(s_users, key=lambda user: (user.vorname, user.nachname))
        p_users = sorted(p_users, key=lambda user: (user.vorname, user.nachname))
        return render(request, 'set_nfc_set/set_nfc_set.html', {"id":tag_id, "s_users":s_users,"p_users":p_users, "tag_username":tag_username})
    return redirect("set_nfc_scan")