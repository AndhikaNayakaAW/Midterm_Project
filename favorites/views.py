# views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Favorite
from main.models import Restaurants
from django.views.decorators.csrf import csrf_exempt

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
