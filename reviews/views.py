# In reviews/views.py
from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from main.models import Restaurants

@login_required
def submit_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Automatically assign the logged-in user
            review.restaurant = restaurant  # Automatically assign the restaurant
            review.save()
            return redirect('main:restaurant_details', id=restaurant.id)  # I added main: infornt of restaurant_details so that it can be redirected to the correct url
    else:
        form = ReviewForm()

    context = {
        'restaurant': restaurant,
        'form': form,
    }
    return render(request, 'reviews/submit_review.html', context)
