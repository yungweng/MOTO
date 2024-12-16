from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Device
from main_app.models import Nutzer
from api.serializers import NutzerSerializer

class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Nutzer haben Zugriff

    def get(self, request):
        # Alle Nutzer abrufen
        users = Nutzer.objects.all()

        # Nutzer mit dem Serializer serialisieren
        serializer = NutzerSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)