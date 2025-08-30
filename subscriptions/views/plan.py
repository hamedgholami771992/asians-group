from rest_framework import viewsets
from subscriptions.models import Plan
from subscriptions.serializers import PlanSerializer
from subscriptions.permissions import IsAdminOrReadOnly

class PlanViewSet(viewsets.ModelViewSet):
    """
    Plans can be listed by any authenticated user,
    but only admins can create/update/delete.
    """
    queryset = Plan.objects.prefetch_related("features").all()
    serializer_class = PlanSerializer
    permission_classes = [IsAdminOrReadOnly]