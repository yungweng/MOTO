from django.shortcuts import redirect, render
from main_app.models import Schueler
def select_student_change_view(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            students = Schueler.objects.select_related('user_id').order_by('user_id__vorname', 'user_id__nachname')
            return render(request, 'change_data_db/select_student.html',{"students" : students})
        return redirect("master_web")
    return redirect("login")