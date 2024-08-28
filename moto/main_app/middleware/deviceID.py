import uuid
from datetime import timedelta
from django.utils import timezone

class DeviceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'device_id' not in request.COOKIES:
            device_id = str(uuid.uuid4())  # Erstelle eine neue eindeutige Kennung
            response = self.get_response(request)
            expires = timezone.now() + timedelta(hours=10) # Jeden Tag neue device_id
            response.set_cookie('device_id', device_id, expires=expires)
        else:
            response = self.get_response(request)

        return response