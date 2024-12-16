from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Personal, Raum_Belegung
from api.serializers import PersonalSerializer

class PersonalListView(APIView):
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Nutzer haben Zugriff

    def get(self, request):
        # Alle Personal-Objekte, die nicht in einer RaumBelegung als Aufsichtsperson sind
        personal_ohne_aufsicht = Personal.objects.exclude(
            id__in=Raum_Belegung.objects.values('aufsichtspersonen')
        )

        # Die Personal-Objekte serialisieren
        serializer = PersonalSerializer(personal_ohne_aufsicht, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)