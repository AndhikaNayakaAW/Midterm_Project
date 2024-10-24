from django.urls import path
from main.views import (
    show_main, create_restaurant_entry, 
    show_xml, show_json, show_xml_by_id, show_json_by_id, 
    register, login_user, logout_user, 
    edit_restaurant, delete_restaurant, 
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-restaurant-entry', create_restaurant_entry, name='create_restaurant_entry'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-restaurant/<uuid:id>', edit_restaurant, name='edit_restaurant'),
    path('delete/<uuid:id>', delete_restaurant, name='delete_restaurant'),
]