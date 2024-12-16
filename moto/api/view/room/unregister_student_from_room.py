from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Aufenthalt, Raum_Belegung, Nutzer, Schueler, Personal

class UnregisterStudentFromRoomView(APIView):
    def post(self, request):
        tablet_id = request.data.get("tablet_id")
        nutzer_id = request.data.get("nutzer_id")
        action = request.data.get('action')  # Benutzeraktion

        if not nutzer_id:
            return Response(
                {"error": "nutzer_id ist erforderlich."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Raum mit dem Tablet identifizieren
        if tablet_id:
            try:
                raum_belegung = Raum_Belegung.objects.get(tablet_id=tablet_id)
            except Raum_Belegung.DoesNotExist:
                return Response(
                    {"error": "Kein Raum mit dieser Tablet-ID gefunden."},
                    status=status.HTTP_404_NOT_FOUND
                )

            raum = raum_belegung.raum

        # Nutzer anhand der tag_id finden
        nutzer = Nutzer.objects.filter(id=nutzer_id).first()
        if not nutzer:
            return Response(
                {"error": "Kein Nutzer mit der angegebenen tag_id gefunden."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Wenn der Nutzer ein Schüler ist
        schueler = Schueler.objects.filter(user_id=nutzer).first()
        if schueler:
            # Aufenthalt des Schülers im Raum finden
            aufenthalt = Aufenthalt.objects.filter(
                schueler_id=schueler,
                zeitraum__endzeit__isnull=True
            ).first()

            if not aufenthalt:
                return Response(
                    {"error": f"Der Schüler {schueler.user_id.vorname} {schueler.user_id.nachname} ist nicht im Raum angemeldet."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Endzeit des Aufenthalts setzen
            aufenthalt.zeitraum.endzeit = datetime.now().time()
            aufenthalt.zeitraum.save()

            schueler.wc = False
            schueler.schulhof = False

            # Aktion des Benutzers auswerten
            if action == "leave_school":
                schueler.angemeldet = False
            elif action == "toilet":
                schueler.wc = True
            elif action == "school_yard":
                schueler.schulhof = True
            schueler.save()

            return Response(
                {"message": f"Schüler {schueler.user_id.vorname} {schueler.user_id.nachname} wurde erfolgreich abgemeldet."},
                status=status.HTTP_200_OK
            )

        # Wenn der Nutzer ein Personalmitglied ist
        personal = Personal.objects.filter(nutzer=nutzer).first()
        if personal and tablet_id:
            if raum_belegung.aufsichtspersonen.filter(id=personal.id).exists():
                raum_belegung.aufsichtspersonen.remove(personal)
                return Response(
                    {"message": f"Personalmitglied {personal.nutzer.vorname} {personal.nutzer.nachname} wurde erfolgreich abgemeldet."},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": f"Das Personalmitglied {personal.nutzer.vorname} {personal.nutzer.nachname} ist nicht als Aufsichtsperson angemeldet."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Weder Schüler noch Personal
        return Response(
            {"error": "Der Nutzer ist weder Schüler noch Personal."},
            status=status.HTTP_400_BAD_REQUEST
        )
