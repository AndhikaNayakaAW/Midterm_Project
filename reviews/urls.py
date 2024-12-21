#reviews/urls.py
from django.urls import path
from .views import submit_review, submit_review_api, get_reviews_by_id, get_reviews_by_name, csrf_token_view

urlpatterns = [
    # Web-based review submission by restaurant ID (UUID)
    path('submit-review/<uuid:restaurant_id>/', submit_review, name='submit_review'),

    # API-based review submission by restaurant ID (UUID)
    path('api/submit-review/<uuid:restaurant_id>/', submit_review_api, name='submit_review_api'),

    # API to get reviews by UUID
    path('api/get-reviews/<uuid:restaurant_id>/', get_reviews_by_id, name='get_reviews_by_id'),

    # API to get reviews by restaurant name
    path('api/get-reviews-by-name/<str:restaurant_name>/', get_reviews_by_name, name='get_reviews_by_name'),

    # CSRF token endpoint
    path('api/csrf/', csrf_token_view, name='csrf_token'),  # CSRF Token Endpoint
]
