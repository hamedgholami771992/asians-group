from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from subscriptions.models import Plan, Feature

User = get_user_model()


class PlanViewSetTest(APITestCase):

    def setUp(self):
        # Create admin and regular users
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )
        self.regular_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="userpass"
        )

        # Create some features
        self.feature1 = Feature.objects.create(name="Unlimited Storage")
        self.feature2 = Feature.objects.create(name="Custom Reports")

        # Create an existing plan
        self.plan = Plan.objects.create(name="Basic Plan")
        self.plan.features.set([self.feature1])

        # URL for list and create
        self.url = reverse("subscriptions:plan-list")  # DRF router basename="plan"

    def test_list_plans_as_authenticated_user(self):
        """Any authenticated user can list plans"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["features"][0]["id"], self.feature1.id)

    def test_list_plans_requires_authentication(self):
        """Unauthenticated users cannot list plans"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_plan_as_admin(self):
        """Admin can create a plan with features"""
        self.client.force_authenticate(user=self.admin_user)
        payload = {
            "name": "Pro Plan",
            "feature_ids": [self.feature1.id, self.feature2.id]
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plan = Plan.objects.get(id=response.data["id"])
        self.assertEqual(plan.name, "Pro Plan")
        self.assertEqual(list(plan.features.values_list("id", flat=True)), [self.feature1.id, self.feature2.id])

    def test_create_plan_as_regular_user(self):
        """Regular user cannot create a plan"""
        self.client.force_authenticate(user=self.regular_user)
        payload = {"name": "Pro Plan", "feature_ids": [self.feature1.id]}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Plan.objects.filter(name="Pro Plan").count(), 0)

    def test_update_plan_as_admin(self):
        """Admin can update plan name and features"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("subscriptions:plan-detail", args=[self.plan.id])
        payload = {
            "name": "Updated Plan",
            "feature_ids": [self.feature2.id]  # Replace features
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Updated Plan")
        self.assertEqual(list(self.plan.features.values_list("id", flat=True)), [self.feature2.id])

    def test_update_plan_as_regular_user(self):
        """Regular user cannot update plan"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("subscriptions:plan-detail", args=[self.plan.id])
        payload = {"name": "Hacked Plan", "feature_ids": [self.feature2.id]}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Basic Plan")

    def test_delete_plan_as_admin(self):
        """Admin can delete a plan"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("subscriptions:plan-detail", args=[self.plan.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Plan.objects.filter(id=self.plan.id).exists())

    def test_delete_plan_as_regular_user(self):
        """Regular user cannot delete a plan"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("subscriptions:plan-detail", args=[self.plan.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Plan.objects.filter(id=self.plan.id).exists())
