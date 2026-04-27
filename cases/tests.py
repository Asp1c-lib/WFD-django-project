from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser
from .models import Case

# Create your tests here.

class CaseModelTests(TestCase):

    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username="user1",
            password="password",
            role="customer"
        )

    def test_case_creation(self):
        """
        Test that a Case can be created successfully
        """
        case = Case.objects.create(
            customer=self.customer,
            title="Headache issue",
            description="Severe headache for 3 days",
            category="Appointment",
            priority="High",
            status="Open"
        )

        self.assertEqual(case.title, "Headache issue")
        self.assertEqual(case.status, "Open")
        self.assertEqual(case.customer.username, "user1")
        
        
    def test_case_status_update(self):
        case = Case.objects.create(
            customer=self.customer,
            title="Billing issue",
            description="Wrong charge",
            category="Billing",
            priority="Medium"
        )

        case.status = "Resolved"
        case.save()

        self.assertEqual(case.status, "Resolved")
        
        
    def test_customer_case_filtering(self):
        Case.objects.create(
            customer=self.customer,
            title="Test Case 1",
            description="Desc",
            category="Other",
            priority="Low"
        )

        Case.objects.create(
            customer=self.customer,
            title="Test Case 2",
            description="Desc",
            category="Other",
            priority="Low"
        )

        cases = Case.objects.filter(customer=self.customer)

        self.assertEqual(cases.count(), 2)
        
        
from django.urls import reverse


class CaseViewTests(TestCase):

    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username="user1",
            password="password",
            role="customer"
        )

    def test_my_cases_page_loads(self):
        self.client.login(username="user1", password="password")

        response = self.client.get(reverse("my_cases"))

        self.assertEqual(response.status_code, 200)
        
class CustomerUseCaseTests(TestCase):

    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username="usercase",
            password="password",
            role="customer"
        )

    def test_customer_can_create_case(self):
        self.client.login(username="usercase", password="password")

        response = self.client.post(
            reverse("create_case"),
            {
                "title": "Test 1",
                "description": "Test 1 desc",
                "category": "Others",
                "priority": "High"
            }
        )

        self.assertEqual(response.status_code, 302)  # redirect
        self.assertEqual(Case.objects.count(), 1)

        case = Case.objects.first()
        self.assertEqual(case.title, "Test 1")
        
class AgentUseCaseTests(TestCase):

    def setUp(self):
        self.customer = CustomUser.objects.create_user(
            username="customer1",
            password="password",
            role="customer"
        )

        self.agent = CustomUser.objects.create_user(
            username="agent1",
            password="password",
            role="agent"
        )

        self.case = Case.objects.create(
            customer=self.customer,
            title="Billing Problem",
            description="Incorrect invoice",
            category="Billing",
            priority="Medium"
        )

    def test_agent_can_view_open_cases(self):
        self.client.login(username="agent1", password="password")

        response = self.client.get("/dashboard/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Billing Problem")