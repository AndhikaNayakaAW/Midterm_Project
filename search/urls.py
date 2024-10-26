from django.urls import path
from search.views import (
    search_restaurants
)

app_name = 'search'

urlpatterns = [
    path('search_restaurants', search_restaurants, name='search_restaurants'),
]