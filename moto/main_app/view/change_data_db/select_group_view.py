from django.shortcuts import redirect, render
from main_app.models import Gruppe
def select_group_change_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            groups = Gruppe.objects.order_by('name')
            return render(request, 'change_data_db/select_group.html',{"groups" : groups})
        return redirect("master_web")
    return redirect("login")