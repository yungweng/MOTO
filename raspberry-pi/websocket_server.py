import asyncio
import websockets
import json

# Liste verbundener WebSocket-Clients
clients = set()

async def handler(websocket, path):
    # Client hinzufügen
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            rfid_id = data.get('rfid_id')
            print(f"NFC-Tag gescannt: {rfid_id}")

            # Sende die NFC-ID an alle verbundenen Clients (Browser)
            for client in clients:
                if client != websocket:
                    await client.send(f"NFC-Scanner: {rfid_id}")
    finally:
        # Entferne den Client, wenn er sich trennt
        clients.remove(websocket)

# Starte den WebSocket-Server
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8000):
        print("WebSocket Server läuft auf Port 8000")
        await asyncio.Future()  # läuft für immer

if __name__ == "__main__":
    asyncio.run(main())
