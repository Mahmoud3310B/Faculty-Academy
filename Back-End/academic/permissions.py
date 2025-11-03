# academic/permissions.py

from rest_framework import permissions
from .models import Instructor

class IsAdministrator(permissions.BasePermission):
    """ السماح بالوصول فقط إذا كان المستخدم مسؤولاً (is_superuser أو is_staff) """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff))

class IsInstructor(permissions.BasePermission):
    """ السماح بالوصول فقط إذا كان المستخدم محاضراً """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Instructor.objects.filter(user=request.user).exists()