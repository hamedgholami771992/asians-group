

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from subscriptions.models import Feature, Plan, Subscription

User = get_user_model()


class FullWorkflowEndToEndTest(APITestCase):

    def setUp(self):
        # --- Users ---
        self.admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpass",
        }
        self.user_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "userpass",
        }

        # Register regular user via API
        self.register_url = reverse("user-list-create")
        resp = self.client.post(self.register_url, self.user_data, format="json")
        self.user = User.objects.get(username=self.user_data["username"])

        # Create admin via ORM
        self.admin = User.objects.create_superuser(
            username=self.admin_data["username"],
            email=self.admin_data["email"],
            password=self.admin_data["password"]
        )

        # Login to obtain JWT tokens
        self.login_url = reverse("user-login")
        login_user = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }, format="json")
        self.user_token = login_user.data["access"]

        login_admin = self.client.post(self.login_url, {
            "username": self.admin_data["username"],
            "password": self.admin_data["password"]
        }, format="json")
        self.admin_token = login_admin.data["access"]

        # Feature & Plan URLs
        self.feature_url = reverse("subscriptions:feature-list")
        self.plan_url = reverse("subscriptions:plan-list")
        self.subscription_url = reverse("subscriptions:subscription-list")

    def test_full_workflow(self):
        """
        Full workflow test:
        1. Admin creates features
        2. Admin creates a plan with features
        3. User subscribes to a plan
        4. User changes plan
        5. User deactivates subscription
        """

        # --- Step 1: Admin creates features ---
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        feature_resp1 = self.client.post(self.feature_url, {"name": "Unlimited API Access"}, format="json")
        feature_resp2 = self.client.post(self.feature_url, {"name": "Priority Support"}, format="json")
        self.assertEqual(feature_resp1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(feature_resp2.status_code, status.HTTP_201_CREATED)
        feature1_id = feature_resp1.data["id"]
        feature2_id = feature_resp2.data["id"]

        # --- Step 2: Admin creates plan with features ---
        plan_payload = {"name": "Pro Plan", "feature_ids": [feature1_id, feature2_id]}
        plan_resp = self.client.post(self.plan_url, plan_payload, format="json")
        self.assertEqual(plan_resp.status_code, status.HTTP_201_CREATED)
        plan_id = plan_resp.data["id"]

        # --- Step 3: User creates subscription ---
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        sub_payload = {"plan_id": plan_id}
        sub_resp = self.client.post(self.subscription_url, sub_payload, format="json")
        self.assertEqual(sub_resp.status_code, status.HTTP_201_CREATED)
        subscription_id = sub_resp.data["id"]

        # --- Step 4: Admin creates another plan for plan change ---
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        plan2_resp = self.client.post(self.plan_url, {"name": "Enterprise Plan", "feature_ids": [feature1_id]}, format="json")
        self.assertEqual(plan2_resp.status_code, status.HTTP_201_CREATED)
        new_plan_id = plan2_resp.data["id"]

        # --- Step 5: User changes subscription plan ---
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        change_url = reverse("subscriptions:subscription-change-plan", args=[subscription_id])
        change_resp = self.client.post(change_url, {"plan_id": new_plan_id}, format="json")
        self.assertEqual(change_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(change_resp.data["plan"]["id"], new_plan_id)

        # --- Step 6: User deactivates subscription ---
        deactivate_url = reverse("subscriptions:subscription-deactivate", args=[subscription_id])
        deactivate_resp = self.client.post(deactivate_url)
        self.assertEqual(deactivate_resp.status_code, status.HTTP_200_OK)

        # Verify in database
        sub = Subscription.objects.get(id=subscription_id)
        self.assertFalse(sub.is_active)
