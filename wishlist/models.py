from django.db import models


# Create your models here.
class Restaurant(models.Model):  # I did the import of data with this one (Naïm)
    name = models.CharField(max_length=255)
    island = models.CharField(max_length=63)
    cuisine = models.CharField(max_length=63)
    gmaps = models.TextField()
    contacts = models.CharField(max_length=63)

    def __str__(self):
        return self.name
