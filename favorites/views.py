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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from uuid import UUID
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken' : csrf_token})

@login_required
def view_favorites(request):
    favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
    
    context = {
        'favorites_items': favorites_items,
    }
    return render(request, 'favorites.html', context)

@login_required
@csrf_exempt
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
@csrf_exempt
def remove_from_favorites(request, restaurant_id):
    favorites_item = get_object_or_404(Favorite, user=request.user, restaurant_id=restaurant_id)
    favorites_item.delete()
    
    message = "Restaurant removed from your favorites."
    
    return JsonResponse({'success': True, 'message': message})

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_favorites_flutter(request):

    try:
        print(f"Headers: {request.headers}")
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")

        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
        favorites_data = [
            {
                "id": favorite.restaurant.id,
                "name": favorite.restaurant.name,
                "category": favorite.restaurant.cuisine,
                "image_url": favorite.restaurant.image,
                "rating": 5,
                "is_favorite":'yes',
                "is_bookmark":'yes'
            }
            for favorite in favorites_items
        ]

        print(favorites_data)
        return Response(favorites_data, status=200)

    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_favorites_flutter(request, restaurant_id):

    try:

        restaurant = get_object_or_404(Restaurants, id=restaurant_id)
        favorites_items, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

        if created:
            message = f"{restaurant.name} has been added to favorites."
        else:
            message = f"{restaurant.name} is already in your favorites."

        favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
        favorites_data = [
            {
                "id": favorite.restaurant.id,
                "name": favorite.restaurant.name,
                "category": favorite.restaurant.cuisine,
                "image_url": favorite.restaurant.image,
                "rating": 5,
            }
            for favorite in favorites_items
        ]

        return Response(
            {
                "success": True,
                "message": message,
                "favorite": favorites_data,
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_favorites_flutter(request, restaurant_id):

    try:
        favorites_item = Favorite.objects.get(user=request.user, restaurant_id=restaurant_id)
        favorites_item.delete()

        favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
        favorites_data = [
            {
                "id": favorite.restaurant.id,
                "name": favorite.restaurant.name,
                "category": favorite.restaurant.cuisine,
                "image_url": favorite.restaurant.image,
                "rating": 5,  
            }
            for favorite in favorites_items
        ]

        return Response(
            {
                "success": True,
                "message": "Restaurant removed from your favorites list!",
                "favorite": favorites_data,
            },
            status=status.HTTP_200_OK
        )

    except Favorite.DoesNotExist:
        return Response(
            {"success": False, "message": "Restaurant is not in your favorites list!"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )