# favorites/urls.py
from django.urls import path
from favorites.views import view_favorites, add_to_favorites, remove_from_favorites, view_favorites_flutter, add_to_favorites_flutter, remove_from_favorites_flutter, csrf_token_view

app_name = 'favorites'

urlpatterns = [
    path('favorites/', view_favorites, name='view_favorites'),
    path('add-to-favorites/<str:restaurant_id>/', add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<str:restaurant_id>/', remove_from_favorites, name='remove_from_favorites'),

    path('api/favorites/', view_favorites_flutter, name='view_favorites_flutter'),
    path('api/add-to-favorites/<str:restaurant_id>/', add_to_favorites_flutter, name='add_to_favorites_flutter'),
    path('api/remove-from-favorites/<str:restaurant_id>/', remove_from_favorites_flutter, name='remove_from_favorites_flutter'),

    path('api/csrf/', csrf_token_view, name='csrf_token'),
]