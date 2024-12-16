from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from main_app.models import Raum_Belegung
from api.serializers import RaumBelegungSerializer
from rest_framework.permissions import IsAuthenticated

# API View
class GetRaumBelegungView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        tablet_id = request.data.get("tablet_id")
        if not tablet_id:
            return Response({"message": "Tablet-ID ist erforderlich."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Raumbelegung anhand der Tablet-ID abrufen
        raum_belegung = get_object_or_404(Raum_Belegung, tablet_id=tablet_id)
        
        # Serialisieren und zurückgeben
        serializer = RaumBelegungSerializer(raum_belegung)
        return Response(serializer.data, status=status.HTTP_200_OK)
