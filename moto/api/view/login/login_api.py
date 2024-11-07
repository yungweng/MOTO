from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from api.models import Device

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    # Holen der Eingabedaten
    username = request.data.get("username")
    password = request.data.get("password")
    device_id = request.data.get("device_id")

    # Überprüfen, ob ein device_id übergeben wurde
    if not device_id:
        return Response({"error": "DeviceID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authentifizieren des Benutzers
    user = authenticate(username=username, password=password)
    if user is not None:
        # JWT-Token generieren
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Überprüfen, ob das Gerät bereits einem Benutzer zugeordnet ist
        existing_device = Device.objects.filter(device_id=device_id).first()

        if existing_device:
            # Wenn das Gerät bereits einem anderen Benutzer zugeordnet ist, löschen wir den alten Eintrag
            if existing_device.user != user:
                existing_device.delete()  # Entfernt die alte Zuordnung des Geräts zum Benutzer

        # Gerät mit dem neuen Benutzer verknüpfen oder aktualisieren
        Device.objects.update_or_create(user=user, device_id=device_id)

        # Erfolgreiche Antwort zurückgeben
        return Response({
            "access_token": access_token,
            "refresh_token": str(refresh),
            "device_id": device_id
        })
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
