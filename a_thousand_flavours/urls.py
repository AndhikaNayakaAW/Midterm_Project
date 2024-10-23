from django.urls import path, include
from main.views import show_main
from search.views import search_restaurants

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("", include("main.urls")),
    path("search/", search_restaurants, name="search_restaurants"),
]
