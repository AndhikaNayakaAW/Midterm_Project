from django.urls import path
from wishlist.views import (
    show_wishlist
)

app_name = 'wishlist'

urlpatterns = [
    path('wish', show_wishlist, name='show_wishlist'),
]