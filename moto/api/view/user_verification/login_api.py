from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from api.serializers import CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    """
    Angepasste Login-View mit OTP-Prüfung.
    """
    serializer_class = CustomTokenObtainPairSerializer