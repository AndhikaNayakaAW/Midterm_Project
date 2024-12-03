from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .forms import ReviewForm
from .serializers import ReviewSerializer
from main.models import Restaurants
from urllib.parse import unquote  # For decoding URL-encoded names
from django.http import Http404

# Web-based functionality for submitting reviews
@login_required
def submit_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assign the logged-in user
            review.restaurant = restaurant  # Assign the restaurant
            review.save()
            return redirect('main:restaurant_details', id=restaurant.id)  # Redirect to restaurant details
    else:
        form = ReviewForm()

    context = {
        'restaurant': restaurant,
        'form': form,
    }
    return render(request, 'reviews/submit_review.html', context)


# API-based functionality for submitting reviews (for Flutter app)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_review_api(request, restaurant_id):
    restaurant_id = unquote(restaurant_id)  # Decode URL-encoded restaurant ID
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)  # Match by UUID
    data = request.data.copy()
    data['user'] = request.user.id
    data['restaurant'] = restaurant.id

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API-based functionality for retrieving reviews for a specific restaurant
@api_view(['GET'])
def get_reviews(request, restaurant_name):
    restaurant = Restaurants.objects.filter(name=restaurant_name).first()
    if not restaurant:
        raise Http404("Restaurant not found")
    reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
