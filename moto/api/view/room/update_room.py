from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from main_app.models import Raum_Belegung, Raum, Personal, Nutzer, AGKategorie, AG

class UpdateRaumBelegungView(APIView):
    def patch(self, request):
        tablet_id = request.data.get("tablet_id")
        if not tablet_id:
            return Response({"message": "Tablet-ID ist erforderlich."}, status=status.HTTP_400_BAD_REQUEST)
        
        raum_belegung = get_object_or_404(Raum_Belegung, tablet_id=tablet_id)

        # Neue AG-Daten
        ag_name = request.data.get("ag_name")
        ag_category_id = request.data.get("ag_category_id")
        max_anzahl = request.data.get("ag_max_anzahl")

        # Validierung der `max_anzahl` gegen Raumkapazität
        if max_anzahl is not None:
            if max_anzahl > raum_belegung.raum.kapazitaet:
                return Response(
                    {"message": "Die maximale Anzahl darf die Kapazität des Raumes nicht überschreiten."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Neue Aufsichtspersonen (IDs aus Nutzer)
        aufsichtspersonen_ids = request.data.get("aufsichtspersonen_ids")
        if aufsichtspersonen_ids is not None:
            # Konvertiere Nutzer-IDs zu Personal-Objekten
            personal_objects = Personal.objects.filter(nutzer__id__in=aufsichtspersonen_ids)
            if personal_objects.count() != len(aufsichtspersonen_ids):
                return Response(
                    {"message": "Einige der angegebenen Nutzer-IDs sind ungültig oder keine Aufsichtspersonen."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Entfernen aller aktuellen Aufsichtspersonen und hinzufügen der neuen
            raum_belegung.aufsichtspersonen.set(personal_objects)
            
            # Sicherstellen, dass mindestens eine Aufsichtsperson vorhanden bleibt
            if raum_belegung.aufsichtspersonen.count() == 0:
                return Response(
                    {"message": "Mindestens eine Aufsichtsperson ist erforderlich."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Änderungen an AG
        if ag_name is not None:
            raum_belegung.ag.name = ag_name

        if ag_category_id is not None:
            ag_category = get_object_or_404(AGKategorie, id=ag_category_id)
            raum_belegung.ag.ag_kategorie = ag_category

        if max_anzahl is not None:
            raum_belegung.ag.max_anzahl = max_anzahl

        # Änderungen speichern
        raum_belegung.ag.save()
        raum_belegung.save()

        return Response({"message": "Raumbelegung erfolgreich aktualisiert."}, status=status.HTTP_200_OK)
