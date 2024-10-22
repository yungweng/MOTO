import time
import websocket
import json
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()
SERVER_WS_URL = "ws://10.67.168.21:8000/ws/nfc/"

def send_rfid_data():
    ws = websocket.WebSocket()
    ws.connect(SERVER_WS_URL)

    try:
        while True:
            print("Halten Sie einen Chip an den Leser")
            id, text = reader.read()
            print(f"ID: {id}")

            data = json.dumps({'rfid_id': id})
            ws.send(data)

            time.sleep(2)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    send_rfid_data()