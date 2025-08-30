# accounts/views/user.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.serializers import UserCreateSerializer, UserSerializer
from accounts.permissions import IsSelfOrAdmin 

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle user operations:
      - Registration
      - Retrieve/Update profile (self)
      - Admin-only promote to superuser
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        # Use different serializers for creation vs. other actions
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """
        - Registration (create) is public
        - Listing all users is admin-only
        - Retrieve/update profile requires authentication
        - Promote requires admin
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["list", "promote"]:
            return [permissions.IsAdminUser()]
        else:  # retrieve, update, partial_update, destroy
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]

    @action(detail=False, methods=["get", "put", "patch"], url_path="me")
    def me(self, request):
        """
        GET /api/accounts/me/ -> Get current user
        PUT/PATCH /api/accounts/me/ -> Update current user
        """
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="promote", permission_classes=[permissions.IsAdminUser])
    def promote(self, request, pk=None):
        """
        POST /api/accounts/{id}/promote/ -> Promote user to superuser (admin-only)
        """
        user = self.get_object()
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return Response(
            {"status": f"User {user.username} promoted to superuser."},
            status=status.HTTP_200_OK,
        )
