## Dependencies

Es müssen Docker und OpenSSL installiert sein.

## self-signed certificate and key

Beim ersten Starten des Servers muss diese Zeile ausgeführt werden und die Fragen beantwortet werden.

Sonst kann keine HTTPS Verbindung aufgebaut werden und es funktioniert die NFC API nicht.

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx-selfsigned.key -out nginx-selfsigned.crt`

## Docker Compose

Der Docker kann durch den unteren Befehl gestartet werden.

`docker-compose up --build`

(Bei Fragen gerne jederzeit bei Yannick melden)
