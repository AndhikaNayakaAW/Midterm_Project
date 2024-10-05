from django.forms import ModelForm
from main.models import Restaurants

class RestoEntryForm(ModelForm):
    class Meta:
        model = Restaurants
        fields = ["Name", "Island", "Cuisine","Description"]