from django.contrib.auth.models import AbstractUser, User
from django.db import models


LIMIT_USERNAME_LENGTH: int = 150


class User(AbstractUser):
    """Модель пользователя."""

    class UserRoles(models.TextChoices):
        """Возможные роли пользователей."""
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    bio = models.TextField(
        'Инф-ия о пользователе',
        max_length=254,
        blank=True,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Статус (роль) пользователя',
        max_length=25,
        choices=UserRoles.choices,
        default=UserRoles.USER,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    def __str__(self) -> str:
        """Строковое представления пользователя."""
        return f'{self.username} ({self.role})'
