from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Raum
from api.serializers import RaumSerializer

class RoomListView(APIView):
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Nutzer haben Zugriff

    def get(self, request):
        raeume = Raum.objects.all()  # Alle Räume abrufen
        serializer = RaumSerializer(raeume, many=True)  # Daten serialisieren
        return Response(serializer.data, status=status.HTTP_200_OK)