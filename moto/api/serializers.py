from rest_framework import status, serializers
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from main_app.models import Nutzer, Raum, Raum_Belegung, Personal, AGKategorie, Raum_Belegung

class NutzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutzer
        fields = ['id', 'vorname', 'nachname', 'tag_id']

class RaumSerializer(serializers.ModelSerializer):
    belegt = serializers.SerializerMethodField()

    class Meta:
        model = Raum
        fields = ['id', 'raum_nr', 'geschoss', 'kapazitaet', 'belegt']  # Hier definierst du die Felder, die zurückgegeben werden sollen

    def get_belegt(self, obj):
        # Prüfen, ob es Raumbelegungen für diesen Raum gibt
        belegung = Raum_Belegung.objects.filter(raum=obj).exists()
        return belegung

class RaumBelegungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raum_Belegung
        fields = ['id', 'tablet_id', 'ag', 'gruppe', 'zeitraum', 'aufsichtspersonen']


class PersonalSerializer(serializers.ModelSerializer):
    # Verwenden des NutzerSerializers, um die notwendigen Felder zu serialisieren
    nutzer = NutzerSerializer()

    class Meta:
        model = Personal
        fields = ['nutzer']  # Wir geben nur das 'nutzer' Feld zurück

class AGKategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = AGKategorie
        fields = ['id', 'name']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Angepasster Serializer für den Token-Login.
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        # Überprüfen, ob der Benutzer ein Personal ist
        user = self.user
        try:
            personal = Personal.objects.get(user=user)
            is_otp = personal.is_password_otp  # Prüfen, ob is_password_otp True ist
        except Personal.DoesNotExist:
            is_otp = False  # Kein Personal -> is_otp auf False setzen

        # Zusätzliche Informationen zur Antwort hinzufügen
        data['is_otp'] = is_otp
        return data
    
class RaumBelegungSerializer(serializers.ModelSerializer):
    raum = serializers.SerializerMethodField()
    ag = serializers.SerializerMethodField()
    aufsichtspersonen = serializers.SerializerMethodField()
    zeitraum = serializers.SerializerMethodField()

    class Meta:
        model = Raum_Belegung
        fields = ["raum", "ag", "aufsichtspersonen", "zeitraum"]

    def get_raum(self, obj):
        return {
            "raum_nr": obj.raum.raum_nr,
            "geschoss": obj.raum.geschoss,
            "kapazitaet": obj.raum.kapazitaet,
        }

    def get_ag(self, obj):
        return {
            "name": obj.ag.name,
            "kategorie": obj.ag.ag_kategorie.name if obj.ag.ag_kategorie else None,
            "max_anzahl": obj.ag.max_anzahl,
        }

    def get_aufsichtspersonen(self, obj):
        return [
            {
                "id": person.nutzer.id,
                "vorname": person.nutzer.vorname,
                "nachname": person.nutzer.nachname,
            }
            for person in obj.aufsichtspersonen.all()
        ]

    def get_zeitraum(self, obj):
        return {
            "startzeit": obj.zeitraum.startzeit.isoformat(),
            "endzeit": obj.zeitraum.endzeit.isoformat() if obj.zeitraum.endzeit else None,
        }