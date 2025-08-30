from rest_framework import serializers
from subscriptions.models import Subscription, Plan
from subscriptions.serializers import PlanSerializer

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)  # nested details
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        source="plan",
        write_only=True
    )

    class Meta:
        model = Subscription
        fields = ["id", "plan", "plan_id", "start_date", "is_active"]
        read_only_fields = ["id", "start_date", "is_active"]

    def validate_plan_id(self, value):
        """
        Prevent changing subscription to the same plan.
        This only applies when updating an existing subscription instance.
        """
        if self.instance and self.instance.plan_id == value.id:
            raise serializers.ValidationError(
                "Cannot change to the same plan."
            )
        return value