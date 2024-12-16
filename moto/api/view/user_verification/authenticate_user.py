from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class AuthenticateUserView(APIView):
    permission_classes = [IsAuthenticated]  # Sicherstellen, dass der Nutzer eingeloggt ist

    def post(self, request, *args, **kwargs):
        # Das Passwort wird im Request erwartet
        password = request.data.get("password")
        user = request.user  # Der aktuell eingeloggte Nutzer, basierend auf dem Request

        # Überprüfen, ob ein Passwort übergeben wurde
        if not password:
            return Response(
                {"message": "Passwort muss übergeben werden."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Überprüfen, ob das angegebene Passwort korrekt ist
        user_check = authenticate(username=user.username, password=password)
        
        # Falls der Nutzer mit dem angegebenen Passwort nicht authentifiziert werden konnte
        if user_check is None:
            return Response(
                {"is_authenticated": False},
                status=status.HTTP_200_OK
            )

        # Falls das Passwort korrekt ist
        return Response(
            {"is_authenticated": True},
            status=status.HTTP_200_OK
        )
