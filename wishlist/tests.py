from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Reserve
from main.models import Restaurants

class WishlistTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.restaurant = Restaurants.objects.create(
            name='Test Restaurant',
            cuisine='Test Cuisine',
            island='Test Island',
            contacts='123456789',
            gmaps='http://maps.google.com',
        )

    def test_add_to_wishlist(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('wishlist:add_to_wishlist', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('main:restaurant_details', args=[self.restaurant.id]))
        self.assertTrue(Reserve.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_add_to_wishlist_already_exists(self):
        self.client.login(username='testuser', password='testpass')
        Reserve.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(reverse('wishlist:add_to_wishlist', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('main:restaurant_details', args=[self.restaurant.id]))
        self.assertEqual(Reserve.objects.filter(user=self.user, restaurant=self.restaurant).count(), 1)

    def test_view_wishlist(self):
        self.client.login(username='testuser', password='testpass')
        Reserve.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.get(reverse('wishlist:view_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Restaurant')

    def test_remove_from_wishlist(self):
        self.client.login(username='testuser', password='testpass')
        wishlist_item = Reserve.objects.create(user=self.user, restaurant=self.restaurant)
        response = self.client.post(reverse('wishlist:remove_from_wishlist', args=[self.restaurant.id]))
        self.assertRedirects(response, reverse('wishlist:view_wishlist'))
        self.assertFalse(Reserve.objects.filter(id=wishlist_item.id).exists())
