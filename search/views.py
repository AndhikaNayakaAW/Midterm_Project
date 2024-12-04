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


from django.http import JsonResponse


def search_restaurants_json(request):
    query = None
    results = []

    if request.method == "GET":
        form = RestaurantSearchEntry(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            # Perform restaurant search
            restaurants = (
                Restaurants.objects.filter(name__icontains=query)
                | Restaurants.objects.filter(island__icontains=query)
                | Restaurants.objects.filter(cuisine__icontains=query)
            )
            # Convert query results to a list of JSON objects
            results = [
                {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "island": restaurant.island,
                    "cuisine": restaurant.cuisine,
                    "contacts": restaurant.contacts,
                    "gmaps": restaurant.gmaps,
                    "image": restaurant.image,
                }
                for restaurant in restaurants
            ]
    else:
        form = RestaurantSearchEntry()

    # Return the results as JSON
    return JsonResponse({"query": query, "results": results})
