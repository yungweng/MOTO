# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status
# from api.models import Device
# from main_app.models import Nutzer
# from api.serializers import NutzerSerializer
# from api.authentication import DeviceIDAuthentication

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])  # Nur authentifizierte Nutzer haben Zugriff
# def get_user_by_id_api(request, id):
#     # Prüfe, ob das Gerät authentifiziert ist
#     device = request.device  # Das Gerät wird durch die DeviceIDAuthentication zur Verfügung gestellt

#     if not device:
#         return Response({"error": "Device is not registered"}, status=status.HTTP_400_BAD_REQUEST)

#     # Das Gerät existiert, nun können wir den Benutzer abrufen
#     try:
#         user = Nutzer.objects.get(id=id)
#     except Nutzer.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     # Nutzer-Daten serialisieren und zurückgeben
#     serializer = NutzerSerializer(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Device
from main_app.models import Nutzer
from api.serializers import NutzerSerializer

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Nur authentifizierte Nutzer haben Zugriff

    def get(self, request, id):
        # Jetzt sollte request.device gesetzt sein, falls die Authentifizierung erfolgreich war
        try:
            user = Nutzer.objects.get(id=id)
        except Nutzer.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NutzerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)