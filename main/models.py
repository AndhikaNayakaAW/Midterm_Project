from django.db import models
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
    
class Quotes(models.Model):
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.content[:50] 
    
class Contact(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    message = models.TextField()