# In your views.py file (in the appropriate app, e.g., main or a dedicated wishlist app)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Reserve
from main.models import Restaurants

@login_required
def add_to_wishlist(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    wishlist_item, created = Reserve.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        # Successfully added to wishlist
        message = f"{restaurant.name} has been added to your wishlist."
    else:
        # Item already exists in the wishlist
        message = f"{restaurant.name} is already in your wishlist."

    return redirect('restaurant_details', id=restaurant.id)  # Redirect to the restaurant detail page

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
    
    return redirect('view_wishlist') 