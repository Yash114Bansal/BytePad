from rest_framework import permissions

class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_faculty or request.user.is_staff)

class IsHOD(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_department_head or request.user.is_staff
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.method in permissions.SAFE_METHODS
        )

class IsFacultyOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_faculty or request.user.is_staff or request.method in permissions.SAFE_METHODS
        )


class IsHODOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_department_head or request.user.is_staff or request.method in permissions.SAFE_METHODS
        )


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student
