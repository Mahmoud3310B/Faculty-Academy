# academic/permissions.py

from rest_framework import permissions
from .models import Instructor

class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff))

class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Instructor.objects.filter(user=request.user).exists()