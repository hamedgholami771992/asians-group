

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Return DRF test client without authentication."""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Helper to create a user quickly."""
    def make_user(**kwargs):
        data = {
            "email": kwargs.get("email", "user@example.com"),
            "password": kwargs.get("password", "testpass123"),
        }
        return User.objects.create_user(
            username=kwargs.get("username", data["email"]),
            email=data["email"],
            password=data["password"],
        )
    return make_user


@pytest.fixture
def auth_client(api_client, create_user):
    """Return APIClient authenticated with a user."""
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client, user
