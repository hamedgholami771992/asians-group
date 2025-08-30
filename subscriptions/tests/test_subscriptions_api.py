from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from subscriptions.models import Plan, Feature, Subscription

User = get_user_model()


class SubscriptionViewSetTest(APITestCase):

    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="pass1234"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="pass1234"
        )

        # Features
        self.feature1 = Feature.objects.create(name="Unlimited Storage")
        self.feature2 = Feature.objects.create(name="Custom Reports")

        # Plans
        self.plan1 = Plan.objects.create(name="Basic Plan")
        self.plan1.features.set([self.feature1])
        self.plan2 = Plan.objects.create(name="Pro Plan")
        self.plan2.features.set([self.feature1, self.feature2])

        # Subscription for user1
        self.subscription1 = Subscription.objects.create(
            user=self.user1,
            plan=self.plan1
        )

        # URLS
        self.list_url =reverse("subscriptions:subscription-list") # remains same, points to /api/subscriptions/subscriptions/
        self.detail_url = lambda pk: reverse("subscriptions:subscription-detail", args=[pk])
        self.change_plan_url = lambda pk: reverse("subscriptions:subscription-change-plan", args=[pk])
        self.deactivate_url = lambda pk: reverse("subscriptions:subscription-deactivate", args=[pk])
    
    def test_list_subscriptions_only_user_owned(self):
        """User sees only their own subscriptions"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["plan"]["id"], self.plan1.id)

        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 0)

    def test_create_subscription(self):
        """User can create subscription for themselves"""
        self.client.force_authenticate(user=self.user2)
        payload = {"plan_id": self.plan2.id}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sub = Subscription.objects.get(user=self.user2)
        self.assertEqual(sub.plan, self.plan2)
        self.assertTrue(sub.is_active)

    def test_change_plan_success(self):
        """User can change their subscription plan"""
        self.client.force_authenticate(user=self.user1)
        payload = {"plan_id": self.plan2.id}
        response = self.client.post(self.change_plan_url(self.subscription1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subscription1.refresh_from_db()
        self.assertEqual(self.subscription1.plan, self.plan2)

    def test_change_plan_same_plan_fails(self):
        """Cannot change to the same plan"""
        self.client.force_authenticate(user=self.user1)
        payload = {"plan_id": self.plan1.id}
        response = self.client.post(self.change_plan_url(self.subscription1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot change to the same plan", str(response.data))

    def test_change_plan_requires_owner(self):
        """Other users cannot change someone else's subscription"""
        self.client.force_authenticate(user=self.user2)
        payload = {"plan_id": self.plan2.id}
        response = self.client.post(self.change_plan_url(self.subscription1.id), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deactivate_subscription(self):
        """User can deactivate their subscription"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.deactivate_url(self.subscription1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subscription1.refresh_from_db()
        self.assertFalse(self.subscription1.is_active)

    def test_deactivate_requires_owner(self):
        """Other users cannot deactivate someone else's subscription"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.deactivate_url(self.subscription1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_subscription_by_owner(self):
        """Owner can delete their subscription"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.detail_url(self.subscription1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(id=self.subscription1.id).exists())

    def test_delete_subscription_by_other_user(self):
        """Other users cannot delete subscription"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.detail_url(self.subscription1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
