from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurants

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    island = models.CharField(max_length=63)
    cuisine = models.CharField(max_length=63)
    contacts = models.CharField(max_length=63) 
    gmaps = models.TextField()
    image = models.TextField(default="")
    
    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"
