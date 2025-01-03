from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Raum
from api.serializers import RaumSerializer
from collections import defaultdict

class RoomListView(APIView):
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Nutzer haben Zugriff

    def get(self, request):
        raeume = Raum.objects.all()  # Alle Räume abrufen
        serializer = RaumSerializer(raeume, many=True)  # Räume serialisieren

        # Räume nach Kategorien gruppieren
        grouped_data = defaultdict(list)
        for raum in serializer.data:
            grouped_data[raum['kategorie']].append(raum)

        # Response formatieren
        response_data = [
            {
                'kategorie': kategorie,
                'raeume': raeume
            }
            for kategorie, raeume in grouped_data.items()
        ]

        return Response(response_data, status=status.HTTP_200_OK)
