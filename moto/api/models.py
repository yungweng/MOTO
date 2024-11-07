from django.contrib.auth.models import User
from django.db import models

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Device {self.device_id} for user {self.user.username}"
