from django.urls import path, include
from search.views import search_restaurants, search_restaurants_json
from django.contrib import admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("", include("favorites.urls")),
    path("", include("wishlist.urls")),
    path("", include("search.urls")),
    path("reviews/", include("reviews.urls")),
    path("search/", search_restaurants, name="search_restaurants"),
    path("search_json/", search_restaurants_json, name="search_restaurants_json"),
    path("auth/", include("authentication.urls")),
]
