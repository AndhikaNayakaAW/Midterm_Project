from django.urls import path
from main.views import (
    show_main, create_mood_entry, show_xml, show_json, show_xml_by_id, show_json_by_id, 
    register, login_user, logout_user, edit_mood, delete_mood, add_mood_entry_ajax,
    add_to_favorites, add_to_wishlist, remove_from_wishlist, add_review, show_favorites,
    show_wishlist, restaurant_of_the_month, search_restaurants, redirect_to_google_maps
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-restaurant-entry', create_mood_entry, name='create_restaurant_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-restaurant/<uuid:id>', edit_restaurant, name='edit_restaurant'),
    path('delete/<uuid:id>', delete_restaurant, name='delete_restaurant'),
    path('create-restaurant-entry-ajax', add_restaurant_entry_ajax, name='add_restaurant_entry_ajax'),
    path('add-to-favorites/<uuid:id>', add_to_favorites, name='add_to_favorites'),
    path('add-to-wishlist/<uuid:id>', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<uuid:id>', remove_from_wishlist, name='remove_from_wishlist'),
    path('add-review/<uuid:id>', add_review, name='add_review'),
    path('favorites/', show_favorites, name='show_favorites'),
    path('wishlist/', show_wishlist, name='show_wishlist'),
    path('restaurant-of-the-month/', restaurant_of_the_month, name='restaurant_of_the_month'),
    path('search/', search_restaurants, name='search_restaurants'),
    path('redirect-to-google-maps/<uuid:id>', redirect_to_google_maps, name='redirect_to_google_maps'),
]