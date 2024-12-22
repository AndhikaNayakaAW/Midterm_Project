from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Reserve
from main.models import Restaurants
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

# Generate and return CSRF token
@ensure_csrf_cookie
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

# Render wishlist view (accessible to all)
@api_view(['GET'])
@permission_classes([AllowAny])
def view_wishlist(request):
    try:
        if request.user.is_authenticated:
            # Authenticated users
            wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
        else:
            # Anonymous users
            wishlist = request.session.get('wishlist', [])
            wishlist_items = Restaurants.objects.filter(id__in=wishlist)

        context = {
            'wishlist_items': wishlist_items,
        }
        return render(request, 'wishlist.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return render(request, 'wishlist.html', {'wishlist_items': []})

# Add a restaurant to the wishlist (accessible to all)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_to_wishlist(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurants, id=restaurant_id)

        if request.user.is_authenticated:
            # Authenticated users
            wishlist_item, created = Reserve.objects.get_or_create(user=request.user, restaurant=restaurant)
            if created:
                message = f"{restaurant.name} has been added to your wishlist."
            else:
                message = f"{restaurant.name} is already in your wishlist."
        else:
            # Anonymous users
            wishlist = request.session.get('wishlist', [])
            if restaurant_id not in wishlist:
                wishlist.append(str(restaurant_id))
                request.session['wishlist'] = wishlist
                message = f"{restaurant.name} has been added to your wishlist."
            else:
                message = f"{restaurant.name} is already in your wishlist."

        return Response({"success": True, "message": message}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Remove a restaurant from the wishlist (accessible to all)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def remove_from_wishlist(request, restaurant_id):
    try:
        if request.user.is_authenticated:
            # Authenticated users
            wishlist_item = Reserve.objects.get(user=request.user, restaurant_id=restaurant_id)
            wishlist_item.delete()
        else:
            # Anonymous users
            wishlist = request.session.get('wishlist', [])
            if restaurant_id in wishlist:
                wishlist.remove(str(restaurant_id))
                request.session['wishlist'] = wishlist
            else:
                return Response({"success": False, "message": "Restaurant is not in your wishlist!"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": True, "message": "Restaurant removed from your wishlist!"}, status=status.HTTP_200_OK)

    except Reserve.DoesNotExist:
        return Response({"success": False, "message": "Restaurant is not in your wishlist!"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API: Retrieve wishlist items for both authenticated and anonymous users
@api_view(['GET'])
@permission_classes([AllowAny])
@csrf_exempt
def view_wishlist_flutter(request):
    try:
        if request.user.is_authenticated:
            # Authenticated users
            wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
        else:
            # Anonymous users
            wishlist = request.session.get('wishlist', [])
            wishlist_items = Restaurants.objects.filter(id__in=wishlist)

        wishlist_data = [
            {
                "id": item.restaurant.id if request.user.is_authenticated else item.id,
                "name": item.restaurant.name if request.user.is_authenticated else item.name,
                "category": item.restaurant.cuisine if request.user.is_authenticated else item.cuisine,
                "image_url": item.restaurant.image if request.user.is_authenticated else item.image,
                "rating": 5,
                "is_favorite": "yes",
                "is_bookmark": "yes",
            }
            for item in wishlist_items
        ]

        return Response(wishlist_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API: Add a restaurant to the wishlist (accessible to all via Flutter)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_to_wishlist_flutter(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurants, id=restaurant_id)

        if request.user.is_authenticated:
            # Authenticated users
            wishlist_item, created = Reserve.objects.get_or_create(user=request.user, restaurant=restaurant)
            message = f"{restaurant.name} has been added to your wishlist." if created else f"{restaurant.name} is already in your wishlist."
        else:
            # Anonymous users
            wishlist = request.session.get('wishlist', [])
            if restaurant_id not in wishlist:
                wishlist.append(str(restaurant_id))
                request.session['wishlist'] = wishlist
                message = f"{restaurant.name} has been added to your wishlist."
            else:
                message = f"{restaurant.name} is already in your wishlist."

        return Response({"success": True, "message": message}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API: Remove a restaurant from the wishlist (accessible to all via Flutter)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def remove_from_wishlist_flutter(request, restaurant_id):
    try:
        if request.user.is_authenticated:
            # Authenticated users
            wishlist_item = Reserve.objects.get(user=request.user, restaurant_id=restaurant_id)
            wishlist_item.delete()
        else:
            # Anonymous users
            wishlist = request.session.get('wishlist', [])
            if restaurant_id in wishlist:
                wishlist.remove(str(restaurant_id))
                request.session['wishlist'] = wishlist
            else:
                return Response({"success": False, "message": "Restaurant is not in your wishlist!"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"success": True, "message": "Restaurant removed from your wishlist!"}, status=status.HTTP_200_OK)

    except Reserve.DoesNotExist:
        return Response({"success": False, "message": "Restaurant is not in your wishlist!"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
