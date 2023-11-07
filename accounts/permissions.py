from rest_framework import permissions

class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):

        user = request.user

        if not user.is_authenticated:
            return False
        
        if user.is_faculty:
            return True

        return False
