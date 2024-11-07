from rest_framework.permissions import BasePermission

class IsAuthenticatedDevice(BasePermission):
    def has_permission(self, request, view):
        return request.user is not None and hasattr(request.user, 'device')