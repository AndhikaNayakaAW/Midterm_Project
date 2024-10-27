from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Favorite
from main.models import Restaurants

# Create your views here.
@login_required
def view_favorites(request):
    favorites_items = Favorite.objects.filter(user=request.user).select_related('restaurant')
    
    context = {
        'favorites_items': favorites_items,
    }
    return render(request, 'favorites.html', context)

@login_required
def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    favorites_item, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        messages.success(request, f"{restaurant.name} has been added to your favorites.")
    else:
        messages.info(request, f"{restaurant.name} is already in your favorites.")

    return redirect('main:restaurant_details', id=restaurant.id)

@login_required
def remove_from_favorites(request, restaurant_id):
    favorites_item = get_object_or_404(Favorite, user=request.user, restaurant_id=restaurant_id)
    favorites_item.delete()
    messages.error(request, "Restaurant removed from your favorites.")
    
    return redirect('favorites:view_favorites')
