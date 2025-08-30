from rest_framework.permissions import BasePermission

class IsSelfOrAdmin(BasePermission):
    """
    Allow access only to self or admin users.
    """
    def has_object_permission(self, request, view, obj):
        # obj here is a User instance
        return bool(
            request.user and (
                request.user.is_superuser or obj == request.user
            )
        )
