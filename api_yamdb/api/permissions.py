from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Право доступа только для администратора"""

    def has_permission(self, request, view):
        "Запрос разрешен только для администратора."
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_staff
        )
