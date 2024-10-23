from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    # Assuming you have a Restaurant model already defined
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name} - {self.rating}"
