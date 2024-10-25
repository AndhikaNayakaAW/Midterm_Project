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
>>>>>>> e958b907177fa812283521c3fb7e8837001bd136
