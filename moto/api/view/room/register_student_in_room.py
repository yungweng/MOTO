from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from main_app.models import Raum_Belegung, Aufenthalt, Zeitraum, Nutzer, Schueler, Personal
from datetime import datetime

class RegisterStudentWithTabletView(APIView):
    """
    API zum Anmelden eines Schülers in einem Raum basierend auf der Tablet-ID.
    """

    def post(self, request):
        tablet_id = request.data.get("tablet_id")
        nutzer_id = request.data.get("nutzer_id")  # Nutzer-ID von Schüler oder Personal

        if not tablet_id or not nutzer_id:
            return Response(
                {"error": "Tablet-ID und Nutzer-ID sind erforderlich"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            raum_belegung = Raum_Belegung.objects.get(tablet_id=tablet_id)
        except Raum_Belegung.DoesNotExist:
            return Response(
                {"error": "Kein Raum mit dieser Tablet-ID ist angemeldet"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prüfen, ob die Nutzer-ID zu einem Schüler gehört
        schueler = Schueler.objects.filter(user_id__id=nutzer_id).first()
        if schueler:
            # Überprüfen, ob der Schüler bereits im Raum angemeldet ist
            if Aufenthalt.objects.filter(
                raum_id=raum_belegung.raum,
                schueler_id=schueler,
                zeitraum__endzeit=None
            ).exists():
                return Response(
                    {"message": f"Der Schüler {schueler.user_id.vorname} {schueler.user_id.nachname} ist bereits im Raum angemeldet.",
                     "student_is_registert":True},
                    status=status.HTTP_200_OK
                )

            # Zeitraum erstellen
            zeitraum = Zeitraum.objects.create(startzeit=datetime.now().time())

            # Aufenthalt erstellen
            Aufenthalt.objects.create(
                tag=now().date(),
                schueler_id=schueler,
                raum_id=raum_belegung.raum,
                zeitraum=zeitraum
            )
            schueler.angemeldet = True
            schueler.save()

            return Response(
                {"message": f"Schüler {schueler.user_id.vorname} {schueler.user_id.nachname} wurde erfolgreich im Raum angemeldet."},
                status=status.HTTP_201_CREATED
            )

        # Prüfen, ob die Nutzer-ID zu einem Personal gehört
        personal = Personal.objects.filter(nutzer__id=nutzer_id).first()
        if personal:
            # Überprüfen, ob das Personal bereits als Aufsichtsperson angemeldet ist
            if raum_belegung.aufsichtspersonen.filter(id=personal.id).exists():
                return Response(
                    {"message": f"Das Personalmitglied {personal.nutzer.vorname} {personal.nutzer.nachname} ist bereits angemeldet."},
                    status=status.HTTP_200_OK
                )

            # Personal als Aufsichtsperson hinzufügen
            raum_belegung.aufsichtspersonen.add(personal)

            return Response(
                {"message": f"Personalmitglied {personal.nutzer.vorname} {personal.nutzer.nachname} wurde erfolgreich am Tablet angemeldet."},
                status=status.HTTP_201_CREATED
            )

        # Falls weder Schüler noch Personal gefunden wurde
        return Response(
            {"error": "Kein Schüler oder Personal mit dieser Nutzer-ID gefunden."},
            status=status.HTTP_404_NOT_FOUND
        )

