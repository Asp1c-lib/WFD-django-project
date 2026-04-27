from django.test import TestCase
from .models import CustomUser

# Create your tests here.

class UserModelTests(TestCase):

    def test_create_customer_user(self):
        user = CustomUser.objects.create_user(
            username="testuser",
            password="password",
            role="customer"
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.role, "customer")
        self.assertTrue(user.check_password("password"))
        
    def test_role_assignment(self):
        user = CustomUser.objects.create_user(
            username="agent1",
            password="password",
            role="agent"
        )

        self.assertEqual(user.role, "agent")
        
        
        
from django.urls import reverse


class AuthTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user1",
            password="password",
            role="customer"
        )

    def test_login_success(self):
        login = self.client.login(username="user1", password="password")

        self.assertTrue(login)

    def test_login_page_access(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        
class SecurityTests(TestCase):

    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username="usersecure",
            password="password",
            role="customer"
        )

    def test_customer_cannot_access_admin_dashboard(self):
        self.client.login(username="usersecure", password="password")

        response = self.client.get("/admin/")

        self.assertNotEqual(response.status_code, 200)