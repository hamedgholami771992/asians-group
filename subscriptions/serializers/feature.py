from rest_framework import serializers
from subscriptions.models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name"]
        read_only_fields = ["id"]
