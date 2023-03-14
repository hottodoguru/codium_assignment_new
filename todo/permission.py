from rest_framework import permissions
from .serializers import TodoSerializerNotAuthenticated

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

    def has_permission(self, request, view):
        if request.method == 'PUT' and 'pk' in view.kwargs:
            # Check if the requesting user is the owner of the todo being modified
            todo = view.queryset.get(pk=view.kwargs['pk'])
            return todo.owner == request.user
        else:
            # For all other methods, allow access
            return True

    def has_object_permission(self, request, view, obj):
        # Allow owners to update their own todos
        if request.method == 'PUT' and obj.owner == request.user:
            return True

        # Allow users to read only the name field of todos they don't own
        if request.method == 'GET' and obj.owner != request.user:
            view.serializer_class = TodoSerializerNotAuthenticated
            return True

        return False