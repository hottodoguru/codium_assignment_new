from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user


class TodoPermission(permissions.BasePermission):
    """
    Custom permission to allow users to update their own todos
    and to read only the name field of todos they don't own.
    """
    def has_object_permission(self, request, view, obj):
        # Allow owners to update their own todos
        if request.method in ['PUT', 'DELETE', 'PATCH'] and obj.owner == request.user:
            return True
        return False
