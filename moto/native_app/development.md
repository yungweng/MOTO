Für die Entwicklung von GTK Anwendungen unter MacOS wird folgendes benötigt:

1. `brew install xquartz`
2. `open -a XQuartz`
Im XQuartz Terminal gebe ein:
3. `xhost +`
4. `xhost +local:`

Danach sollte das GTK Fenster in XQuartz mit `docker compose up` angezeigt werden