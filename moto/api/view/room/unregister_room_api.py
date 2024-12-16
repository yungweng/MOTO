from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Raum_Belegung, Aufenthalt, Raum_Historie, Zeitraum
from datetime import datetime

class UnregisterTabletView(APIView):
    """
    API zum Abmelden eines Tablets aus einem Raum.
    """
    def post(self, request):
        # Tablet-ID aus dem Request-Daten
        tablet_id = request.data.get("tablet_id")
        
        if not tablet_id:
            return Response({"error": "Tablet-ID ist erforderlich"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Raumbelegung für das Tablet abrufen
            raum_belegung = Raum_Belegung.objects.get(tablet_id=tablet_id)
        except Raum_Belegung.DoesNotExist:
            return Response({"error": "Das Tablet ist nicht in einem Raum angemeldet"}, status=status.HTTP_404_NOT_FOUND)
        
        # Zugehörigen Raum abrufen
        raum = raum_belegung.raum
        
        # Aufenthalte im Raum mit offenem Zeitraum (kein Endzeitpunkt) beenden
        offene_aufenthalte = Aufenthalt.objects.filter(raum_id=raum, zeitraum__endzeit=None)
        for aufenthalt in offene_aufenthalte:
            aufenthalt.zeitraum.endzeit = datetime.now().time()
            aufenthalt.zeitraum.save()
        
        # Zeitraum der Raumbelegung beenden
        zeitraum = raum_belegung.zeitraum
        zeitraum.endzeit = datetime.now().time()
        zeitraum.save()
        
        # Raum-Historie-Eintrag erstellen
        Raum_Historie.objects.create(
            zeitraum=zeitraum,
            raum=raum,
            tag=datetime.now().date(),
            ag_name=raum_belegung.ag.name,
            ag_kategorie=raum_belegung.ag.ag_kategorie,
            leiter=raum_belegung.ag.leiter,
            max_anzahl=raum_belegung.ag.max_anzahl
        )
        
        # Raumbelegung löschen
        raum_belegung.delete()
        
        return Response({"message": "Tablet erfolgreich abgemeldet"}, status=status.HTTP_200_OK)
