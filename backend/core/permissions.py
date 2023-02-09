from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
