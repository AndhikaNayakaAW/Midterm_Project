from django.urls import path, include
from search.views import search_restaurants
from django.contrib import admin


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("search/", search_restaurants, name="search_restaurants"),
]
