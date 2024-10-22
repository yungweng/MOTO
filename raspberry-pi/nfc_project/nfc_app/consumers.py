import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NFCConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'rfid_group',  # Beispiel-Gruppenname
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'rfid_group',  # Beispiel-Gruppenname
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        rfid_id = data['rfid_id']
        await self.channel_layer.group_send(
            'rfid_group',
            {
                'type': 'rfid_message',
                'message': rfid_id
            }
        )

    async def rfid_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
