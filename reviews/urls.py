from django.urls import path
from .views import submit_review, submit_review_api, get_reviews

urlpatterns = [
    path('submit-review/<uuid:restaurant_id>/', submit_review, name='submit_review'),
    path('api/submit-review/<uuid:restaurant_id>/', submit_review_api, name='submit_review_api'),
    path('api/get-reviews/<uuid:restaurant_id>/', get_reviews, name='get_reviews'),
]
