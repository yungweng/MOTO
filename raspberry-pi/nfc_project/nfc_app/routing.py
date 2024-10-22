from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/nfc/', consumers.NFCConsumer.as_asgi()),
]
