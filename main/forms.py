from django.forms import ModelForm
from main.models import Restaurants,Contact

class RestoEntryForm(ModelForm):
    class Meta:
        model = Restaurants
        fields = ["name", "island", "cuisine","contacts","gmaps","image"]

class ContactUsForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "message"]
