from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
import re
from main_app.models import Personal

class ChangePasswordView(APIView):
    """
    View, um das Passwort eines authentifizierten Nutzers zu ändern.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Authentifizierter Nutzer
        authenticated_user = request.user

        # Hole Personal-Eintrag für den Nutzer
        try:
            personal = Personal.objects.get(user=authenticated_user)
        except Personal.DoesNotExist:
            return Response(
                {"message": "Nutzer konnte nicht gefunden werden."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Hole alte und neue Passwörter aus der Anfrage
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # Validierung: Neues Passwort muss angegeben werden
        if not new_password:
            return Response(
                {"message": "Das neue Passwort muss angegeben werden."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validierung: Passwortstärke prüfen
        def validate_password_strength(password):
            if len(password) < 8:
                return "Das Passwort muss mindestens 8 Zeichen lang sein."
            if not re.search(r"[A-Z]", password):
                return "Das Passwort muss mindestens einen Großbuchstaben enthalten."
            if not re.search(r"[a-z]", password):
                return "Das Passwort muss mindestens einen Kleinbuchstaben enthalten."
            if not re.search(r"[0-9]", password):
                return "Das Passwort muss mindestens eine Zahl enthalten."
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                return "Das Passwort muss mindestens ein Sonderzeichen enthalten."
            return None

        error = validate_password_strength(new_password)
        if error:
            return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)

        # Prüfe, ob das alte Passwort benötigt wird
        if personal.is_password_otp:
            # OTP-Modus: Kein altes Passwort erforderlich
            personal.is_password_otp = False  # Zurücksetzen des OTP-Status
        else:
            # Validierung: Altes Passwort muss übergeben werden
            if not old_password:
                return Response(
                    {"message": "Das alte Passwort muss angegeben werden."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Überprüfe das alte Passwort
            if not check_password(old_password, authenticated_user.password):
                return Response(
                    {"message": "Das alte Passwort ist inkorrekt."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Neues Passwort setzen
        authenticated_user.password = make_password(new_password)
        authenticated_user.save()

        # Rückgabe einer Erfolgsmeldung
        return Response(
            {"message": "Das Passwort wurde erfolgreich geändert."},
            status=status.HTTP_200_OK,
        )
