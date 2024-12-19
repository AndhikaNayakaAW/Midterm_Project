from django.urls import path
from wishlist.views import (
    add_to_wishlist, view_wishlist, remove_from_wishlist, view_wishlist_flutter, add_to_wishlist_flutter, remove_from_wishlist_flutter, csrf_token_view
)

app_name = 'wishlist'

urlpatterns = [
    path('add-to-wishlist/<str:restaurant_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('remove-from-wishlist/<str:restaurant_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('api/wishlist/', view_wishlist_flutter, name='view_wishlist_flutter'),
    path('api/add-to-wishlist/<str:restaurant_id>/', add_to_wishlist_flutter, name='add_to_wishlist_flutter'),
    path('api/remove-from-wishlist/<str:restaurant_id>/', remove_from_wishlist_flutter, name='remove_from_wishlist_flutter'),
    path('api/csrf/', csrf_token_view, name='csrf_token'),
]