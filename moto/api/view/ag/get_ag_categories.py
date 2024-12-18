from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from main_app.models import AGKategorie
from api.serializers import AGKategorieSerializer

class AGKategorieListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Alle AG-Kategorien abrufen
        ag_kategorien = AGKategorie.objects.all()
        
        # Serialisieren der AG-Kategorien
        serializer = AGKategorieSerializer(ag_kategorien, many=True)
        
        # Rückgabe der serialisierten Daten
        return Response(serializer.data, status=status.HTTP_200_OK)
