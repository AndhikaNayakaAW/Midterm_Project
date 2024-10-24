from django.urls import path, include
from favorites.views import show_all_tuples

app_name = "favorites"

urlpatterns = [
    path("favoritesall/", show_all_tuples, name="show_main"),
]
