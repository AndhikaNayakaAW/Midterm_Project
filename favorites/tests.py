from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Restaurants
from .models import Favorite

class FavoritesTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.restaurant = Restaurants.objects.create(
            name='Test Restaurant',
            cuisine='Test Cuisine',
            island='Test Island',
            contacts='123456789',
            gmaps='http://maps.google.com',
        )

    def test_view_favorites(self):
        self.client.login(username='testuser', password='testpass')
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(reverse('favorites:view_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')

    def test_add_to_favorites(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('favorites:add_to_favorites', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('main:restaurant_details', args=[self.restaurant.id]))
        self.assertTrue(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_add_to_favorites_already_exists(self):
        self.client.login(username='testuser', password='testpass')
        Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(reverse('favorites:add_to_favorites', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('main:restaurant_details', args=[self.restaurant.id]))
        self.assertEqual(Favorite.objects.filter(user=self.user, restaurant=self.restaurant).count(), 1)

    def test_remove_from_favorites(self):
        self.client.login(username='testuser', password='testpass')
        favorites_item = Favorite.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.post(reverse('favorites:remove_from_favorites', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('favorites:view_favorites'))
        self.assertFalse(Favorite.objects.filter(id=favorites_item.id).exists())
