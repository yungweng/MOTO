import hashlib
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

        # JSON-Daten in einen String konvertieren
        serialized_data = serializer.data
        serialized_data_str = str(serialized_data).encode('utf-8')

        # ETag aus den Daten generieren (Hash des JSON-Inhalts)
        etag = hashlib.md5(serialized_data_str).hexdigest()

        # Prüfen, ob der Client das ETag sendet
        client_etag = request.headers.get('If-None-Match')
        if client_etag == etag:
            # Daten haben sich nicht geändert -> Status 304 zurückgeben
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        # Daten mit ETag zurückgeben
        return Response(serializer.data, status=status.HTTP_200_OK, headers={'ETag': etag})
