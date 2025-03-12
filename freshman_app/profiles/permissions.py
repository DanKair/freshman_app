from rest_framework.permissions import BasePermission

class IsFreshman(BasePermission):
    """Allows access only to Freshman users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "freshman"

class IsMentor(BasePermission):
    """Allows access only to Mentor users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "mentor"

class IsApplicant(BasePermission):
    """Allows access only to Freshman users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "applicant"