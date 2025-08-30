from rest_framework import viewsets
from subscriptions.models import Feature
from subscriptions.serializers import FeatureSerializer
from subscriptions.permissions import IsAdminOrReadOnly

class FeatureViewSet(viewsets.ModelViewSet):
    """
    Features can be listed by any authenticated user,
    but only admins can create/update/delete.
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [IsAdminOrReadOnly]