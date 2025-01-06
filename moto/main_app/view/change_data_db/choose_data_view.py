from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from main_app.models import Personal, Gruppe

def choose_data_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            return render(request, 'change_data_db/choose_data.html')
        return redirect("master_web")
    else:
        return redirect("login")