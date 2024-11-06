from django.http import JsonResponse
from main_app.models import Schueler, Nutzer

def api_get_name_of_id(request, id):
    data = {"message": "Keinen Nutzer gefunden!"}
    if request.method == "GET":
        device_id = request.headers.get('Client-Device-ID')
        print(device_id)
        if Nutzer.objects.filter(id=id).exists():
            nutzer = Nutzer.objects.get(id=id)
            data = {"message": nutzer.vorname + " " + nutzer.nachname}
    return JsonResponse(data)