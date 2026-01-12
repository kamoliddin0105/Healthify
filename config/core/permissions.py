from rest_framework import permissions


class UniversalPermission(permissions.BasePermission):
    """
    Permission Controller
    """

    actions_tool = {
        'list': 'VIEW',
        'retrieve': 'VIEW',
        'create': 'CREATE',
        'update': 'UPDATE',
        'partial_update': 'UPDATE',
        'destroy': 'DELETE',
    }

    def has_permission(self, request, view):
        user = request.user
        available_permissions = user.role.values_list('role_permissions__permission', flat=True)
        action = self.actions_tool[view.get_action() if not hasattr(view, 'action') else view.action]

        needed_role = f'{action}_{view.router_name}'
        return needed_role in available_permissions


class DigitAgroPermission(permissions.BasePermission):
    """
    Permission class for DigitAgro group
    """

    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return user.groups.filter(name='DIGIT_AGRO').exists()
        return False
