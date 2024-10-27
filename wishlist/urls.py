from django.urls import path
from wishlist.views import (
    add_to_wishlist, view_wishlist, remove_from_wishlist
)

app_name = 'wishlist'

urlpatterns = [
    path('add-to-wishlist/<str:restaurant_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('remove-from-wishlist/<str:restaurant_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]