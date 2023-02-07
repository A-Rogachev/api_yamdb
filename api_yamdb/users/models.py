from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    class UserRoles(models.TextChoices):
        """Возможные роли пользователей."""

        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

    bio = models.TextField(
        'Инф-ия о пользователе',
        max_length=settings.LIMIT_USER_BIO_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.LIMIT_USER_EMAIL_LENGTH,
        unique=True,
    )
    role = models.CharField(
        'Статус (роль) пользователя',
        max_length=settings.LIMIT_USER_ROLE_LENTGH,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    @property
    def is_admin(self):
        """Пользователь имеет права администратора."""
        return (
            self.role == self.UserRoles.ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        """Пользователь имеет права модератора."""
        return (
            self.role == self.UserRoles.MODERATOR
            or self.is_staff
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    def __str__(self) -> str:
        """Строковое представления пользователя."""
        return f'{self.username} ({self.role})'