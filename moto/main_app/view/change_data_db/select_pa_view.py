from django.shortcuts import redirect, render
from main_app.models import Personal
def select_pa_change_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            pas = Personal.objects.select_related('nutzer').order_by('nutzer__vorname', 'nutzer__nachname')
            return render(request, 'change_data_db/select_pa.html',{"pas" : pas})
        return redirect("master_web")
    return redirect("login")