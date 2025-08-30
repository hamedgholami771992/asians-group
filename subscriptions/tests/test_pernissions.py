import pytest
from rest_framework import status
from subscriptions.models import Subscription

@pytest.mark.django_db
def test_other_user_cannot_change_subscription(auth_client, create_user):
    owner = create_user(username="owner", email="owner@example.com", password="pass")
    sub = Subscription.objects.create(user=owner, plan_id=1, is_active=True)

    other_user_client = auth_client(username="other", email="other@example.com", password="pass")
    url = f"/subscriptions/{sub.id}/change_plan/"
    response = other_user_client.post(url, {"plan_id": 1})
    assert response.status_code == status.HTTP_403_FORBIDDEN
