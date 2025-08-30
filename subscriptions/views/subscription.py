from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from subscriptions.models.subscription import Subscription
from subscriptions.serializers.subscription import SubscriptionSerializer
from ..permissions import IsOwnerOfSubscription

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Manage subscriptions for the authenticated user.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfSubscription]

    def get_queryset(self):
        """
        Limit to current user's subscriptions.
        Optimize with select_related & prefetch_related.
        """
        qs = Subscription.objects.select_related("plan").prefetch_related("plan__features")
        if self.action == "list":
            return qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        """
        When creating, bind subscription to the logged-in user.
        """
        serializer.save(user=self.request.user)



    @action(detail=True, methods=["post"], url_path="change-plan")
    def change_plan(self, request, pk=None):
        """
        Custom action: Change a subscription's plan.
        POST /subscriptions/{id}/change-plan/
        Body: { "plan_id": X }
        """
        subscription = self.get_object()
        plan_id = request.data.get("plan_id")

        if not plan_id:
            return Response({"error": "plan_id required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(
            subscription,
            data={'plan_id': plan_id},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        """
        Custom action: Deactivate a subscription.
        POST /subscriptions/{id}/deactivate/
        """
        subscription = self.get_object()
        subscription.is_active = False
        subscription.save(update_fields=["is_active"])
        return Response({"status": "subscription deactivated"})
