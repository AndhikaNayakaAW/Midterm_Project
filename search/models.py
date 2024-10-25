from django.db import models
<<<<<<< HEAD
import uuid


class Restaurants(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    island = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    contacts = models.CharField(max_length=100)
    gmaps = models.TextField()
    image = models.TextField(default="")

    def __str__(self):
        return self.name
=======
from main.models import Restaurants
>>>>>>> 41ccd8aaa19f4472922b1bb8a47266564094e8ba
