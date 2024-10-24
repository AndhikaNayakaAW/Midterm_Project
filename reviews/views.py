from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Restaurant
from .forms import ReviewForm

def create_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form, 'restaurant': restaurant})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)
    return render(request, 'reviews/restaurant_detail.html', {'restaurant': restaurant, 'reviews': reviews})

