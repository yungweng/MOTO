# gtk_app/Dockerfile
FROM python:3.12

# Setze Umgebungsvariablen
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installiere Systempakete inklusive der Abhängigkeiten für PyGObject
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-gi python3-gi-cairo \
    gir1.2-gtk-3.0 x11-apps gobject-introspection libgirepository1.0-dev libcairo2-dev \
    pkg-config build-essential && \
    apt-get clean

# Kopiere und installiere die Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Anwendungscode
WORKDIR /app

# Starte die Anwendung
CMD ["python3", "main.py"]
