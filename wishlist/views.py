from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserve
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
def view_wishlist(request):
    wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required
@csrf_exempt
def add_to_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    wishlist_item, created = Reserve.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        messages.success(request, f"{restaurant.name} has been added to your wishlist.")
    else:
        messages.info(request, f"{restaurant.name} is already in your wishlist.")

    return redirect('main:restaurant_details', id=restaurant.id)

@login_required
@csrf_exempt
def remove_from_wishlist(request, restaurant_id):
    wishlist_item = get_object_or_404(Reserve, user=request.user, restaurant_id=restaurant_id)
    wishlist_item.delete()
    messages.error(request, "Item removed from your wishlist.")
    
    return redirect('wishlist:view_wishlist')

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_wishlist_flutter(request):
    try:
        print(f"Headers: {request.headers}")
        print(f"Authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")

        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
        wishlist_data = [
            {
                "id": item.restaurant.id,
                "name": item.restaurant.name,
                "category": item.restaurant.cuisine,
                "image_url": item.restaurant.image,
                "rating": 5,
                "is_bookmark":'yes'
            }
            for item in wishlist_items
        ]

        print(wishlist_data)
        return Response(wishlist_data, status=200)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist_flutter(request, restaurant_id):
    try:
        
        # Get the restaurant object
        restaurant = get_object_or_404(Restaurants, id=restaurant_id)

        # Add the restaurant to the user's wishlist
        wishlist_item, created = Reserve.objects.get_or_create(user=request.user, restaurant=restaurant)

        if created:
            message = f"{restaurant.name} has been added to your wishlist."
        else:
            message = f"{restaurant.name} is already in your wishlist."

        # Fetch the updated wishlist
        wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
        wishlist_data = [
            {
                "id": item.restaurant.id,
                "name": item.restaurant.name,
                "category": item.restaurant.cuisine,
                "image_url": item.restaurant.image,
                "rating": 5,  # Replace with actual rating if available
            }
            for item in wishlist_items
        ]

        return Response(
            {
                "success": True,
                "message": message,
                "wishlist": wishlist_data,
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
def remove_from_wishlist_flutter(request, restaurant_id):
    try:
        # Get the wishlist item for the user and the specific restaurant
        wishlist_item = Reserve.objects.get(user=request.user, restaurant_id=restaurant_id)
        wishlist_item.delete()

        # Fetch the updated wishlist
        wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
        wishlist_data = [
            {
                "id": item.restaurant.id,
                "name": item.restaurant.name,
                "category": item.restaurant.cuisine,
                "image_url": item.restaurant.image,
                "rating": 5,  # Replace with actual rating if available
                
            }
            for item in wishlist_items
        ]

        return Response(
            {
                "success": True,
                "message": "Restaurant removed from your wishlist!",
                "wishlist": wishlist_data,
            },
            status=status.HTTP_200_OK
        )

    except Reserve.DoesNotExist:
        return Response(
            {"success": False, "message": "Restaurant is not in your wishlist!"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
