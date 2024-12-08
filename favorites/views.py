# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Favorite
from main.models import Restaurants
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@login_required
def view_favorites(request):
    favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
    
    context = {
        'favorites_items': favorites_items,
    }
    return render(request, 'favorites.html', context)

@login_required
@csrf_exempt  # Only if necessary for your AJAX calls
def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    favorites_item, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        message = f"{restaurant.name} has been added to your favorites."
        success = True
    else:
        message = f"{restaurant.name} is already in your favorites."
        success = False

    return JsonResponse({'success': success, 'message': message})

@login_required
@csrf_exempt  # Only if necessary for your AJAX calls
def remove_from_favorites(request, restaurant_id):
    favorites_item = get_object_or_404(Favorite, user=request.user, restaurant_id=restaurant_id)
    favorites_item.delete()
    
    message = "Restaurant removed from your favorites."
    
    return JsonResponse({'success': True, 'message': message})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_favorites_flutter(request):
    favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
    favorites_data = [
        {
            "id": favorite.restaurant.id,
            "name": favorite.restaurant.name,
            "island": favorite.restaurant.island,
            "cuisine": favorite.restaurant.cuisine,
            "gmaps": favorite.restaurant.gmaps,
            "contacts": favorite.restaurant.contacts,
        }
        for favorite in favorites_items
    ]

    return Response(favorites_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites_flutter(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    favorites_item, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        return Response(
            {"success": True, "message": f"{restaurant.name} has been added to your favorites!"},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {"success": False, "message": f"{restaurant.name} is already in your favorites!"},
            status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_favorites_flutter(request, restaurant_id):
    try:
        favorites_item = Favorite.objects.get(user=request.user, restaurant_id=restaurant_id)
        favorites_item.delete()
        return Response(
            {"success": True, "message": "Restaurant removed from your favorites!"},
            status=status.HTTP_200_OK
        )
    except Favorite.DoesNotExist:
        return Response(
            {"success": False, "message": "Restaurant is not in your favorites!"},
            status=status.HTTP_404_NOT_FOUND
        )