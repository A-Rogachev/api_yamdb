from django.contrib.auth.models import AbstractUser, User
from django.db import models

from .validators import validate_year

LIMIT_USERNAME_LENGTH: int = 150


class User(AbstractUser):
    """Модель пользователя."""

    class UserRoles(models.TextChoices):
        """Возможные роли пользователей."""
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

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

    @property
    def is_admin(self):
        """Пользователь имеет права администратора."""
        return (
            self.role == self.UserRoles.ADMIN
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        """Пользователь имеет права модератора."""
        return self.role == self.UserRoles.MODERATOR

    @property
    def is_user(self):
        """Пользователь является обычным пользователем."""
        return self.role == self.UserRoles.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    def __str__(self) -> str:
        """Строковое представления пользователя."""
        return f'{self.username} ({self.role})'


class Category(models.Model):
    """Модель категории один к одному"""
    name = models.CharField(
        'Название категории',
        unique=True,
        max_length=256
    )
    slug = models.SlugField(
        'Слаг категории',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанры один ко многим"""
    name = models.CharField(
        'Название жанра',
        unique=True,
        max_length=256
    )
    slug = models.SlugField(
        'Слаг жанра',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Основная модель"""
    name = models.CharField(
        'Название',
        max_length=256
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(
        'Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        # through='TitleGenre',
        related_name='titles',
        verbose_name='Жанр',
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


# class TitleGenre(models.Model):
#     genre = models.ForeignKey(
#         Genre,
#         on_delete=models.SET_NULL,
#         null=True
#     )
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.SET_NULL,
#         null=True
#     )


class Review(models.Model):

    class ScoreChoice(models.IntegerChoices):
        TERRIBLE = 1
        WILDLY = 2
        NIGHTMATE = 3
        BLOODCURDLING = 4
        POORLY = 5
        NO_BAD = 6
        FINE = 7
        GOOD = 8
        GREAT = 9
        PERFECT = 10

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews",
    )
    score = models.IntegerField(
        choices=ScoreChoice.choices,
        default=ScoreChoice.TERRIBLE,
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
