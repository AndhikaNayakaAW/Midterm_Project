from django.urls import path
from search.views import search_restaurants, search_restaurants_json

app_name = "search"

urlpatterns = [
    path("search_restaurants", search_restaurants, name="search_restaurants"),
    path(
        "search_restaurants_json",
        search_restaurants_json,
        name="search_restaurants_json",
    ),
]
