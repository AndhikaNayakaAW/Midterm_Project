from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    @classmethod
    def from_json(cls, json_data):
        return cls(
            username=json_data.get('username', 'No username available'),
            email=json_data.get('email', 'No email available'),
            password=json_data.get('password', 'No password available'),
        )