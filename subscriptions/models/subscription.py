from django.db import models
from django.conf import settings
from django.db.models import Q
from .base import BaseModel
from .plan import Plan


class Subscription(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,           # <-- use settings
        on_delete=models.CASCADE,
        related_name="subscriptions",
        db_index=True,
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        db_index=True,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["plan"]),
        ]
        constraints = [
            # Exactly one active subscription per user
            models.UniqueConstraint(
                fields=["user"],
                condition=Q(is_active=True),
                name="uniq_active_subscription_per_user",
            ),
        ]

    def __str__(self):
        return f"{self.user} -> {self.plan}"
