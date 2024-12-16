from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from main_app.models import Raum, Raum_Belegung
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_rooms_api(request):
    try:
        # Get all rooms ordered by room number
        rooms = Raum.objects.all().order_by('raum_nr')

        # Get current room occupancy
        current_occupancy = Raum_Belegung.objects.filter(
            zeitraum__endzeit__isnull=True
        ).values_list('raum_id', flat=True)

        # Format room data
        room_data = []
        for room in rooms:
            room_data.append({
                'id': room.id,
                'raum_nr': room.raum_nr,
                'geschoss': room.geschoss,
                'kapazitaet': room.kapazitaet,
                'is_occupied': room.id in current_occupancy
            })

        return Response(room_data)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )