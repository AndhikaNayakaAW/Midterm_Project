from django.shortcuts import render
from .models import Restaurants
from .forms import RestaurantSearchEntry


def search_restaurants(request):
    query = None
    results = []

    if request.method == "GET":
        form = RestaurantSearchEntry(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = (
                Restaurants.objects.filter(name__icontains=query)
                | Restaurants.objects.filter(island__icontains=query)
                | Restaurants.objects.filter(cuisine__icontains=query)
            )

    else:
        form = RestaurantSearchEntry()

    context = {"form": form, "query": query, "results": results}

    return render(request, "search.html", context)
