from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from main.models import Restaurants, Quotes, Contact
from reviews.models import Review
import datetime
from user_role.views import create_user_groups

class ViewTests(TestCase):
    def setUp(self):
        # Create user groups before each test
        create_user_groups()
        
        # Create users
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin_user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
        
        # Assign the admin user to the Admin group
        admin_group = Group.objects.get(name='Admin')
        self.admin_user.groups.add(admin_group)

        # Create other test data
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
    
    def test_show_xml_by_user(self):
        self.client.login(username="testuser", password="testpass")  # Log in as a regular user
        response = self.client.get(reverse("main:show_xml"))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect for regular users
        self.assertRedirects(response, '/unauthorized/?next=/xml/', fetch_redirect_response=False)

    def test_show_xml_by_admin(self):
        self.client.login(username="admin", password="adminpass")  # Log in as an admin user
        response = self.client.get(reverse("main:show_xml"))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response for admin users
        self.assertEqual(response["Content-Type"], "application/xml")  # Ensure correct content type

    def test_show_json_by_user(self):
        self.client.login(username="testuser", password="testpass")  # Log in as a regular user
        response = self.client.get(reverse("main:show_json"))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect for regular users
        self.assertRedirects(response, '/unauthorized/?next=/json/', fetch_redirect_response=False)

    def test_show_json_by_admin(self):
        self.client.login(username="admin", password="adminpass")  # Log in as an admin user
        response = self.client.get(reverse("main:show_json"))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response for admin users
        self.assertEqual(response["Content-Type"], "application/json")  # Ensure correct content type
    
    def test_show_xml_by_id_user(self):
        self.client.login(username="testuser", password="testpass")  # Log in as a regular user
        response = self.client.get(reverse("main:show_xml_by_id", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect for regular users
        self.assertRedirects(response, f'/unauthorized/?next=/xml/{self.restaurant.id}/', fetch_redirect_response=False)

    def test_show_xml_by_id_admin(self):
        self.client.login(username="admin", password="adminpass")  # Log in as an admin user
        response = self.client.get(reverse("main:show_xml_by_id", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response for admin users
        self.assertEqual(response["Content-Type"], "application/xml")  # Ensure correct content type

    def test_show_json_by_id_user(self):
        self.client.login(username="testuser", password="testpass")  # Log in as a regular user
        response = self.client.get(reverse("main:show_json_by_id", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect for regular users
        self.assertRedirects(response, f'/unauthorized/?next=/json/{self.restaurant.id}/', fetch_redirect_response=False)

    def test_show_json_by_id_admin(self):
        self.client.login(username="admin", password="adminpass")  # Log in as an admin user
        response = self.client.get(reverse("main:show_json_by_id", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)  # Expecting a successful response for admin users
        self.assertEqual(response["Content-Type"], "application/json")  # Ensure correct content type
    
    def test_register(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newuser",
            "password1": "NewSecurePassword123!",  # Use a more complex password
            "password2": "NewSecurePassword123!",
            "group": "User"  # Ensure this matches your form
        })

        # Print form errors if the status code is not what you expect
        if response.status_code != 302:
            print(response.content)  # Print the response content for debugging
            print(response.context['form'].errors)  # Check for form errors

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


    
    def test_login_user(self):
        response = self.client.post(reverse("main:login_user"), {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 302)
    
    def test_logout_user(self):
        response = self.client.get(reverse("main:logout_user"))
        self.assertEqual(response.status_code, 302)
    
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
