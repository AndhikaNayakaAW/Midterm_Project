from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    island = models.CharField(max_length=63)
    cuisine = models.CharField(max_length=63)
    gmaps = models.TextField()
    contacts = models.CharField(max_length=63)
