from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "userpass",
            "first_name": "Regular",
            "last_name": "User"
        }

        self.admin_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": "adminpass"
        }

        # Register regular user via API
        self.register_url = reverse("user-list-create")
        resp = self.client.post(self.register_url, self.user_data, format="json")
        self.user_id = resp.data["id"]

        # Create admin user directly
        self.admin = User.objects.create_superuser(**self.admin_data)

        # JWT login
        login_url = reverse("user-login")
        user_login = self.client.post(login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        }, format="json")
        self.user_token = user_login.data["access"]

        admin_login = self.client.post(login_url, {
            "username": self.admin_data["username"],
            "password": self.admin_data["password"]
        }, format="json")
        self.admin_token = admin_login.data["access"]

        # URLs
        self.me_url = reverse("user-me")
        self.user_list_url = reverse("user-list-create")
        self.promote_url = lambda pk: reverse("user-promote", args=[pk])
        self.user_detail_url = lambda pk: reverse("user-detail", args=[pk])

    def test_user_registration(self):
        """Public user registration works"""
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass",
            "first_name": "New",
            "last_name": "User"
        }
        resp = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", resp.data)

    def test_me_endpoint_get_and_patch(self):
        """User can retrieve and update their own profile"""
        # GET /me
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        resp = self.client.get(self.me_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["username"], self.user_data["username"])

        # PATCH /me
        patch_payload = {"first_name": "Updated"}
        resp = self.client.patch(self.me_url, patch_payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["first_name"], "Updated")

    def test_regular_user_cannot_list_or_promote(self):
        """Regular user cannot list users or promote others"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        # List users
        resp = self.client.get(self.user_list_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Try to promote self
        resp = self.client.post(self.promote_url(self.user_id))
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_and_promote(self):
        """Admin can list all users and promote a user to superuser"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

        # List users
        resp = self.client.get(self.user_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 2)  # user + admin

        # Promote regular user
        resp = self.client.post(self.promote_url(self.user_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("promoted to superuser", resp.data["status"])

        # Verify in DB
        user = User.objects.get(pk=self.user_id)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_detail_retrieve_update(self):
        """User can retrieve/update own detail (detail endpoint)"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        # GET detail
        resp = self.client.get(self.user_detail_url(self.user_id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["username"], self.user_data["username"])

        # PATCH detail
        resp = self.client.patch(self.user_detail_url(self.user_id), {"last_name": "Changed"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["last_name"], "Changed")

    def test_permissions_enforced_on_detail(self):
        """Regular user cannot update another user's profile"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        resp = self.client.patch(self.user_detail_url(self.admin.id), {"last_name": "Hacker"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
