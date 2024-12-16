from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime
from main_app.models import Schueler, Feedback, Nutzer

class FeedbackSubmissionView(APIView):
    """
    View, die es Schülern ermöglicht, ein Feedback abzugeben.
    Jeder Schüler darf pro Tag ein normales Feedback und ein Mensa-Feedback abgeben.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Hole die Nutzer-ID, das Feedback und den Feedback-Typ aus der Anfrage
        nutzer_id = request.data.get("nutzer_id")
        feedback_wert = request.data.get("feedback_wert")
        mensa_feedback = request.data.get("mensa_feedback", False)  # Standardmäßig normales Feedback

        # Validierung: Nutzer-ID und Feedback-Wert müssen angegeben werden
        if not nutzer_id or not feedback_wert:
            return Response(
                {"message": "Nutzer-ID und Feedback-Wert müssen angegeben werden."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Überprüfen, ob der Nutzer existiert
        try:
            nutzer = Nutzer.objects.get(id=nutzer_id)
        except Nutzer.DoesNotExist:
            return Response(
                {"message": "Ein Nutzer mit der angegebenen ID wurde nicht gefunden."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Überprüfen, ob der Nutzer ein Schüler ist
        try:
            schueler = Schueler.objects.get(user_id=nutzer)
        except Schueler.DoesNotExist:
            return Response(
                {"message": "Der Nutzer ist kein Schüler."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Überprüfen, ob der Schüler für diesen Tag bereits Feedback abgegeben hat
        heutiges_datum = date.today()
        feedback_query = Feedback.objects.filter(
            schueler_id=schueler, 
            tag=heutiges_datum, 
            mensa_feedback=mensa_feedback
        )

        if feedback_query.exists():
            feedback_typ = "Mensa-Feedback" if mensa_feedback else "normales Feedback"
            return Response(
                {"message": f"Der Schüler hat heute bereits ein {feedback_typ} abgegeben."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Erstelle das neue Feedback
        Feedback.objects.create(
            feedback_wert=feedback_wert,
            tag=heutiges_datum,
            zeit=datetime.now().time(),  # Optional: Zeit kann übergeben werden
            schueler_id=schueler,
            mensa_feedback=mensa_feedback,
        )

        feedback_typ = "Mensa-Feedback" if mensa_feedback else "normales Feedback"
        return Response(
            {"message": f"{feedback_typ} wurde erfolgreich abgegeben."},
            status=status.HTTP_201_CREATED,
        )
