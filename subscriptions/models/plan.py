from django.db import models
from .base import BaseModel
from .feature import Feature


class Plan(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    features = models.ManyToManyField(
        Feature,
        related_name="plans",
        blank=True
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
