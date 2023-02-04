from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Право доступа авторизованному пользователь или только чтение"""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """Право доступа только для администратора"""

    def has_permission(self, request, view):
        "Запрос разрешен только для администратора."
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_staff
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Право доступа администратора. Иначе доступно для чтения."""

    def has_permission(self, request, view):
        "Запрос разрешен только для администратора."
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False

    def has_object_permission(self, request, view, obj):
        "Запрос разрешен только для администратора."
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
