#reviews/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .forms import ReviewForm
from .serializers import ReviewSerializer
from main.models import Restaurants
from urllib.parse import unquote  # For decoding URL-encoded names
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from uuid import UUID
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


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
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_review_api(request, restaurant_id):
    try:
        # Remove or comment out this block:
        # if not request.user.is_authenticated:
        #     return Response({"error": "User is not authenticated."},
        #                     status=status.HTTP_401_UNAUTHORIZED)

        restaurant = get_object_or_404(Restaurants, id=restaurant_id)
        data = request.data.copy()
        data['restaurant_id'] = str(restaurant.id)
        serializer = ReviewSerializer(data=data)

        if serializer.is_valid():
            # If you really need a user, handle anonymous cases here, e.g.:
            # if request.user.is_authenticated:
            #     serializer.save(user=request.user)
            # else:
            #     serializer.save(user=None)  # Make user nullable in the model if needed
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Fetch reviews by restaurant ID (UUID)
@api_view(['GET'])
def get_reviews_by_id(request, restaurant_id):
    restaurant = get_object_or_404(Restaurants, id=restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# Fetch reviews by restaurant name
@api_view(['GET'])
def get_reviews_by_name(request, restaurant_name):
    print(f"Fetching reviews for restaurant name: {restaurant_name}")  # Debugging log
    restaurant_name = unquote(restaurant_name).strip()
    restaurant = Restaurants.objects.filter(name__iexact=restaurant_name).first()
    if not restaurant:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
    reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)