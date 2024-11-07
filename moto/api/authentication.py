from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Device

class DeviceIDAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Hole die 'device_id' aus den Headern
        device_id = request.headers.get('Device-ID')  # Beachte: Der Header sollte "Device-ID" statt "device_id" heißen!

        if not device_id:
            return None  # Keine Authentifizierung, wenn kein Device-ID-Header vorliegt

        try:
            # Suche nach dem Gerät mit der entsprechenden ID
            device = Device.objects.get(device_id=device_id)

            # Setze das Gerät in den Request-Context, um später darauf zugreifen zu können
            request.device = device
            return (device.user, None)  # Gibt den authentifizierten Benutzer zurück

        except Device.DoesNotExist:
            raise AuthenticationFailed("Unauthenticated device.")  # Fehler, falls das Gerät nicht gefunden wurde
