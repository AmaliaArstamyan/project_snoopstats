from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the user
    remember_password = models.BooleanField(default=False)  # Store the "Remember Password" checkbox state

    def __str__(self):
        return f"Settings for {self.user.username}"
