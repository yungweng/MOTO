from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="login")
def set_nfc_scan_view(request):
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        if not tag_id == None or not tag_id == "":
            request.session['tag_id'] = tag_id
            return redirect("set_nfc_set")

    return render(request, "master_android/set_nfc_scan.html")