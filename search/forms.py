from django import forms


class RestaurantSearchEntry(forms.Form):
    query = forms.CharField(label="search", max_length=100)
