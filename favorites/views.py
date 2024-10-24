from django.shortcuts import render
from favorites.models import Restaurant


# Create your views here.
def show_all_tuples(request):
    tuples = Restaurant.objects.all()
    return render(request, "templatetest.html", {"tuples": tuples})
