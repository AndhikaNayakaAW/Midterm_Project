from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import Restaurants, Quotes, Contact
from reviews.models import Review
import datetime

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
        self.restaurant = Restaurants.objects.create(name="Test Restaurant")
        self.quote = Quotes.objects.create(content="Test Quote")
        self.client.login(username="testuser", password="testpass")
    
    def test_show_main(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("resto_entries", response.context)
    
    def test_pagination_json(self):
        response = self.client.get(reverse("main:pagination_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
    
    def test_create_restaurant_entry(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("main:create_restaurant_entry"), {"name": "New Restaurant"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Restaurants.objects.filter(name="New Restaurant").exists())
    
    def test_show_xml(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("main:show_xml"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
    
    def test_show_json(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("main:show_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
    
    def test_show_xml_by_id(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("main:show_xml_by_id", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/xml")
    
    def test_show_json_by_id(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(reverse("main:show_json_by_id", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
    
    def test_edit_restaurant(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("main:edit_restaurant", args=[self.restaurant.id]), {"name": "Updated Restaurant"})
        self.assertEqual(response.status_code, 302)
        self.restaurant.refresh_from_db()
        self.assertEqual(self.restaurant.name, "Updated Restaurant")
    
    def test_delete_restaurant(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("main:delete_restaurant", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Restaurants.objects.filter(id=self.restaurant.id).exists())
    
    def test_register(self):
        response = self.client.post(reverse("main:register"), {"username": "newuser", "password1": "newpassword", "password2": "newpassword"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
    
    def test_login_user(self):
        response = self.client.post(reverse("main:login_user"), {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("last_login", self.client.cookies)
    
    def test_logout_user(self):
        response = self.client.get(reverse("main:logout_user"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("last_login", self.client.cookies)
    
    def test_restaurant_details(self):
        response = self.client.get(reverse("main:restaurant_details", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("restaurant", response.context)
    
    def test_create_restaurant_review(self):
        response = self.client.post(reverse("main:create_restaurant_review", args=[self.restaurant.id]), {"rating": 5, "description": "Great!"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(restaurant=self.restaurant, user=self.user).exists())
    
    def test_submit_quote(self):
        response = self.client.post(reverse("main:submit_quote"), {"content": "New Quote"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Quotes.objects.filter(content="New Quote").exists())
    
    def test_show_contact(self):
        response = self.client.get(reverse("main:show_contact"))
        self.assertEqual(response.status_code, 200)
    
    def test_contact_request(self):
        response = self.client.post(reverse("main:contact_request"), {"name": "John", "email": "john@example.com", "message": "Hello!"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(name="John").exists())
