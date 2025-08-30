from rest_framework import permissions

class IsOwnerOfSubscription(permissions.BasePermission):
    """
    Allows access only to the owner of the subscription object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow only admins/superusers to create/update/delete.
    Other authenticated users can only read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and (request.user.is_staff or request.user.is_superuser)