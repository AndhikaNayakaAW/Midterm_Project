from django.db import models
...
from django.contrib.auth.models import User
...
import uuid

class Restaurants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    Name = models.CharField(max_length=100)
    Cuisine = models.CharField(max_length=100)
    Island = models.CharField(max_length=100)
    Description = models.TextField()

    def __str__(self):
        return self.Name
