# favorites/urls.py
from django.urls import path
from favorites.views import view_favorites, add_to_favorites, remove_from_favorites

app_name = 'favorites'

urlpatterns = [
    path('favorites/', view_favorites, name='view_favorites'),
    path('add-to-favorites/<str:restaurant_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<str:restaurant_id>/', remove_from_favorites, name='remove_from_favorites'),
]
