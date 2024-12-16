from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Raum
from api.serializers import RaumSerializer

class RaumDetailView(APIView):
    def get(self, request, raum_id):
        try:
            # Raum-Objekt basierend auf der ID abrufen
            raum = Raum.objects.get(id=raum_id)
        except Raum.DoesNotExist:
            return Response({"error": "Raum not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialisierung des Raum-Objekts
        serializer = RaumSerializer(raum)
        return Response(serializer.data, status=status.HTTP_200_OK)