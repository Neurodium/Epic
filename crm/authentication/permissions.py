from rest_framework.permissions import BasePermission

class IsManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='manager').exists():
            return True
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='manager').exists():
            return True
        if request.user.is_superuser:
            return True
        return False


class IsSales(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='sales').exists():
            return True
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='sales').exists():
            return True
        if request.user.is_superuser:
            return True
        return False


class IsSupport(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='support').exists():
            return True
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='support').exists():
            return True
        if request.user.is_superuser:
            return True
        return False
