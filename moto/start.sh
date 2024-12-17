#!/bin/bash

# Umgebung automatisch erkennen und DISPLAY setzen
if [[ "$(uname -n)" == *"raspberrypi"* ]]; then
    export DISPLAY=:0
else
    export DISPLAY=host.docker.internal:0
fi

# Prüfen, ob ein Argument (Servicename) übergeben wurde
if [ -n "$1" ]; then
    echo "Starte nur den Service: $1"
    docker-compose up -d "$1"
else
    echo "Starte alle Services"
    docker-compose up -d
fi
