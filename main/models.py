from django.db import models
import uuid


class Restaurants(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    island = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField(default="")
    gmaps = models.TextField()


class Restaurant(models.Model):  # I did the import of data with this one (Naïm)
    name = models.CharField(max_length=255)
    island = models.CharField(max_length=63)
    cuisine = models.CharField(max_length=63)
    gmaps = models.TextField()
    contacts = models.CharField(max_length=63)

    def __str__(self):
        return self.name
