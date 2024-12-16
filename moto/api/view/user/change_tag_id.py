from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Nutzer

class AssignTagIDView(APIView):
    """
    View, um einem bestimmten Nutzer (per nutzer_id) eine neue TagID zuzuweisen.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Hole die nutzer_id und die neue TagID aus der Anfrage
        nutzer_id = request.data.get("nutzer_id")
        new_tag_id = request.data.get("tag_id")

        # Validierung: Nutzer-ID und TagID müssen angegeben werden
        if not nutzer_id or not new_tag_id:
            return Response(
                {"message": "Nutzer-ID und TagID müssen angegeben werden."},
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

        # Prüfen, ob die TagID bereits einem anderen Nutzer gehört
        existing_nutzer = Nutzer.objects.filter(tag_id=new_tag_id).exclude(id=nutzer.id).first()
        if existing_nutzer:
            # Lösche die TagID des anderen Nutzers
            existing_nutzer.tag_id = None
            existing_nutzer.save()

        # Zuweisung der neuen TagID an den ausgewählten Nutzer
        nutzer.tag_id = new_tag_id
        nutzer.save()

        return Response(
            {
                "message": f"Die neue TagID '{new_tag_id}' wurde erfolgreich zugewiesen.",
                "nutzer_id": nutzer.id,
                "tag_id": new_tag_id,
            },
            status=status.HTTP_200_OK,
        )
