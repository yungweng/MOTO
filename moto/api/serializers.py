from rest_framework import serializers
from main_app.models import Nutzer

class NutzerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutzer
        fields = ['id', 'vorname', 'nachname', 'tag_id']