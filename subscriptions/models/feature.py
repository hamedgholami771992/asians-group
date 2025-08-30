from django.db import models
from .base import BaseModel


class Feature(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name



