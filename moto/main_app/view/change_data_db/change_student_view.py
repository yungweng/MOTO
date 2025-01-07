from django.shortcuts import redirect, render
from main_app.models import Schueler
def student_change_view(request, id):
    if request.user.is_authenticated:
        user = request.user
        if user.is_superuser:
            print(id)
            student = Schueler.objects.get(id=id)
            return render(request, 'change_data_db/change_student.html',{"student" : student})
        return redirect("master_web")
    return redirect("login")