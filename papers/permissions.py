from rest_framework import permissions

class IsFacultyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_faculty or request.method in permissions.SAFE_METHODS)

class IsHODOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_department_head or request.method in permissions.SAFE_METHODS)
