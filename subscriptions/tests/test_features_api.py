from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from subscriptions.models import Feature

User = get_user_model()


class FeatureViewSetTest(APITestCase):

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )

        # Create regular user
        self.regular_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="userpass"
        )

        # Create some features
        self.feature1 = Feature.objects.create(name="Unlimited Storage")
        self.feature2 = Feature.objects.create(name="Custom Reports")

        # URL for list and create
        self.url = reverse("subscriptions:feature-list")  # DRF router sets "basename-list"

    def test_list_features_as_authenticated_user(self):
        """Any authenticated user can list features"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_features_requires_authentication(self):
        """Unauthenticated users cannot list features"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_feature_as_admin(self):
        """Admin can create a feature"""
        self.client.force_authenticate(user=self.admin_user)
        payload = {"name": "Priority Support"}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feature.objects.count(), 3)
        self.assertEqual(Feature.objects.get(id=response.data["id"]).name, "Priority Support")

    def test_create_feature_as_regular_user(self):
        """Regular user cannot create a feature"""
        self.client.force_authenticate(user=self.regular_user)
        payload = {"name": "Priority Support"}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Feature.objects.count(), 2)

    def test_update_feature_as_admin(self):
        """Admin can update a feature"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("subscriptions:feature-detail", args=[self.feature1.id])
        payload = {"name": "Updated Feature"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.feature1.refresh_from_db()
        self.assertEqual(self.feature1.name, "Updated Feature")

    def test_update_feature_as_regular_user(self):
        """Regular user cannot update a feature"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("subscriptions:feature-detail", args=[self.feature1.id])
        payload = {"name": "Updated Feature"}
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.feature1.refresh_from_db()
        self.assertEqual(self.feature1.name, "Unlimited Storage")

    def test_delete_feature_as_admin(self):
        """Admin can delete a feature"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("subscriptions:feature-detail", args=[self.feature1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Feature.objects.count(), 1)

    def test_delete_feature_as_regular_user(self):
        """Regular user cannot delete a feature"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse("subscriptions:feature-detail", args=[self.feature1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Feature.objects.count(), 2)
