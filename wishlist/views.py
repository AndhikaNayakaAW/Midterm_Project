from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Reserve
from main.models import Restaurants

@login_required
def add_to_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    wishlist_item, created = Reserve.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        messages.success(request, f"{restaurant.name} has been added to your wishlist.")
    else:
        messages.info(request, f"{restaurant.name} is already in your wishlist.")

    return redirect('main:restaurant_details', id=restaurant.id)

@login_required
def view_wishlist(request):
    wishlist_items = Reserve.objects.filter(user=request.user).select_related('restaurant')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required
def remove_from_wishlist(request, restaurant_id):
    wishlist_item = get_object_or_404(Reserve, user=request.user, restaurant_id=restaurant_id)
    wishlist_item.delete()
    messages.error(request, "Item removed from your wishlist.")
    
    return redirect('wishlist:view_wishlist')  
