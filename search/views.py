from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchEntry


def search_restaurants(request):
    query = request.GET.get("query")
    if query:
        results = (
            Restaurant.objects.filter(name__icontains=query)
            | Restaurant.objects.filter(island__icontains=query)
            | Restaurant.objects.filter(cuisine__icontains=query)
        )
    else:
        results = Restaurant.objects.none()  # Empty QuerySet if no query

    context = {
        "form": RestaurantSearchEntry(),
        "query": query,
        "results": results,
    }
    return render(request, "search.html", context)


def search_restaurants_v2(request):
    form = RestaurantSearchEntry()
    results = []
    query = ""

    if query in request.GET:
        query = request.GET["query"]
        results = (
            Restaurant.objects.filter(name__icontains=query)
            | Restaurant.objects.filter(island__icontains=query)
            | Restaurant.objects.filter(cuisine_type__icontains=query)
        )
    return render(
        request, "search.html", {"form": form, "results": results, "query": query}
    )
