from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if getattr(request.user, 'role', None) == 'admin':
            return True

        action = getattr(view, 'action', None) or request.method.lower()
        permissions = getattr(view, 'role_permissions', {})
        allowed_roles = permissions.get(action, permissions.get('*', []))
        return request.user.role in allowed_roles

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
