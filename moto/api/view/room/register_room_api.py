from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from main_app.models import Raum, Raum_Belegung, AG, Zeitraum, Personal, AGKategorie

class RegisterTabletToRoom(APIView):
    """
    API-Endpoint zur Anmeldung eines Tablets in einem Raum.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        tablet_id = data.get("tablet_id")
        raum_id = data.get("raum_id")
        aufsichtsperson_id = data.get("aufsichtsperson_id")
        max_anzahl = data.get("max_anzahl")
        ag_kategorie_name = data.get("activity_kategorie_name")
        activity_name = data.get("activity_name")

        # Validierung der Eingangsdaten
        if not all([tablet_id, raum_id, aufsichtsperson_id, max_anzahl, ag_kategorie_name, activity_name]):
            return Response({"error": "Alle Felder sind erforderlich"}, status=status.HTTP_400_BAD_REQUEST)

        # Überprüfung, ob der Raum existiert
        try:
            raum = Raum.objects.get(id=raum_id)
        except Raum.DoesNotExist:
            return Response({"error": "Raum existiert nicht"}, status=status.HTTP_404_NOT_FOUND)

        # Überprüfung, ob die Kapazität passt
        try:
            max_anzahl = int(max_anzahl)
            if max_anzahl <= 0 or max_anzahl > raum.kapazitaet:
                return Response({"error": f"Kapazität muss zwischen 1 und {raum.kapazitaet} liegen"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Kapazität muss eine Zahl sein"}, status=status.HTTP_400_BAD_REQUEST)

        # Überprüfung, ob die AG-Kategorie existiert
        try:
            ag_kategorie = AGKategorie.objects.get(name=ag_kategorie_name)
        except AGKategorie.DoesNotExist:
            return Response({"error": "AG-Kategorie existiert nicht"}, status=status.HTTP_404_NOT_FOUND)

        # Überprüfung, ob die Aufsichtsperson existiert
        try:
            aufsichtsperson = Personal.objects.get(id=aufsichtsperson_id)
        except Personal.DoesNotExist:
            return Response({"error": "Aufsichtsperson existiert nicht"}, status=status.HTTP_404_NOT_FOUND)

        # Überprüfung, ob der Raum bereits belegt ist
        if Raum_Belegung.objects.filter(raum=raum).exists():
            return Response({"error": "Raum ist bereits belegt"}, status=status.HTTP_400_BAD_REQUEST)

        # Überprüfung, ob das Tablet bereits angemeldet ist
        if Raum_Belegung.objects.filter(tablet_id=tablet_id).exists():
            return Response({"error": "Tablet ist bereits angemeldet"}, status=status.HTTP_400_BAD_REQUEST)

        # Erstellung der AG und der Raumbelegung
        zeitraum = Zeitraum.objects.create(startzeit=datetime.now().time(), endzeit=None)
        ag = AG.objects.create(
            name=activity_name,
            max_anzahl=max_anzahl,
            offene_AG=True,
            leiter=aufsichtsperson,
            ag_kategorie=ag_kategorie
        )
        raum_belegung = Raum_Belegung.objects.create(
            raum=raum,
            ag=ag,
            tablet_id=tablet_id,
            zeitraum=zeitraum
        )
        raum_belegung.aufsichtspersonen.add(aufsichtsperson)

        return Response({"message": "Tablet erfolgreich angemeldet", "raum_id": raum.id}, status=status.HTTP_201_CREATED)
