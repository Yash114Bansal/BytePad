from rest_framework import permissions

class IsFacultyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        user = request.user

        if not user.is_authenticated:
            return False
        
        if user.is_faculty or request.method in permissions.SAFE_METHODS:
            return True

        return False
