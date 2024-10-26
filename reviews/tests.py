from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review
from main.models import Restaurants
from .forms import ReviewForm
import uuid

class ReviewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.restaurant = Restaurants.objects.create(
            id=uuid.uuid4(), 
            name='Test Restaurant',
            island='Test Island',
            cuisine='Test Cuisine',
            contacts='123456789',
            gmaps='https://maps.google.com/?q=Test+Restaurant',
            image='test_image.jpg'
        )

    def test_review_form_validation(self):
        form_data = {'rating': 5, 'description': 'Great food!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data_invalid = {'rating': 6, 'description': 'Out of range rating'}  # rating beyond 5
        form_invalid = ReviewForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())

    def test_submit_review_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('submit_review', args=[self.restaurant.id]), {
            'rating': 4,
            'description': 'Good food and service.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_submit_review_unauthenticated_user(self):
        response = self.client.post(reverse('submit_review', args=[self.restaurant.id]), {
            'rating': 4,
            'description': 'Good food and service.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_redirect_after_review_submission(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('submit_review', args=[self.restaurant.id]), {
            'rating': 5,
            'description': 'Excellent experience!'
        })
        expected_url = reverse('main:restaurant_details', args=[self.restaurant.id])
        self.assertRedirects(response, expected_url)

