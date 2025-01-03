# Aufsetzten des Django Servers:

!! Docker Desktop muss immer währendessen geöffnet sein

## Beim erstenmal um die Docker und die Datenbank zu erstellen (einmalig)
    cmd in Konsole (im selben Ordner wie docker-compose.yml) : docker-compose up --build

## Dannach zum Server starten
    cmd in Konsole (im selben Ordner wie docker-compose.yml) : docker-compose up

## Datenbank zurücksetzten
    Bei fehlern wie 'relation does exists' oder 'column does not exists' kann es sinnvoll sein die Datenbank zurückzusetzten
    1. Docker Desktop öffnen
    2. Containers links oben öffnen
    3. MOTO ausklappen und db-1 mit symbol starten, dannach auf den namen db-1 klicken
    4. Reiter Exec öffnen
    5. cmd eingeben: dropdb moto -f -U postgres
    6. cmd eingeben: createdb moto -U postgres
    7. im Projekt Ordner main_app/migrations alle datein löschen außer __init__.py
    8. mit dem cmd docker-compose up server neustarten, falls der server läuft vorher stoppen   

## Root user erstellen und Datenbank importieren
    1. Server starten
    2. Docker Desktop öffnen
    3. MOTO auswählen und django-1 öffnen
    4. Reiter Exec öffnen
    5. cmd eingeben und dannach weitere daten eingeben (email kann einfach mit enter übergangen werden): python manage.py createsuperuser
    !! Dieser User ist nicht zum Benutzen der einzelnen Funktionen gedacht, sondern rein zur Verwaltung des Backend, Daten und Personal-Nutzer
    6. https://127.0.0.1:8000 im Browser öffnen
    7. mit root user anmelden
    8. CSV-Import auswählen
    9. .xlsx datei auswählen und rechts alle vier Felder auswählen
    10. Datei Hochladen -> Dannach sollte Automatisch eine .xlsx Datei heruntergeladen werden in der die OTPs zu den verschieden Nutzern besteht
    11. Ausloggen und mit neuen Nutzern anmelden 