from rest_framework import serializers
from subscriptions.models import Plan, Feature
from subscriptions.serializers import FeatureSerializer

class PlanSerializer(serializers.ModelSerializer):
    # Read nested details
    features = FeatureSerializer(many=True, read_only=True)
    # Writeable IDs for creation/updating
    feature_ids = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(),
        many=True,
        write_only=True,
        source="features"   # this maps to the M2M field
    )

    class Meta:
        model = Plan
        fields = ["id", "name", "features", "feature_ids"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        features = validated_data.pop("features", [])
        plan = Plan.objects.create(**validated_data)
        plan.features.set(features)
        return plan

    def update(self, instance, validated_data):
        features = validated_data.pop("features", None)
        plan = super().update(instance, validated_data)
        if features is not None:
            plan.features.set(features)
        return plan
