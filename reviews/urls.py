from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/review/', views.create_review, name='create_review'),
]
