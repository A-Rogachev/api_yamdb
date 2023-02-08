from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_year

User = get_user_model()


class UnitedGenreCategory(models.Model):
    """Добавляет поля для моделей Category и Genre."""
    name = models.CharField(
        'Название',
        unique=True,
        max_length=settings.LIMIT_NAME_LENGHT
    )
    slug = models.SlugField(
        'Слаг',
        max_length=settings.LIMIT_SLUG_LENGHT,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        """Строковое представление."""
        return self.name


class Category(UnitedGenreCategory):
    """Модель категории произведения."""

    class Meta(UnitedGenreCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(UnitedGenreCategory):
    """Модель жанра произведения."""

    class Meta(UnitedGenreCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        'Название',
        max_length=settings.LIMIT_NAME_LENGHT
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=(validate_year,)
    )
    description = models.TextField(
        'Описание'
    )
    genre = models.ManyToManyField(
        Genre,
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
        """Строковое представления произведения."""
        return self.name


class BaseReviewsComments(models.Model):
    """Базовый класс для моделей отзывов и комментариев."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        default_related_name = '%(model_name)ss'


class Review(BaseReviewsComments):
    """Модель отзыва на произведение."""

    class ScoreChoice(models.IntegerChoices):
        """Возможные оценки."""

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

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        choices=ScoreChoice.choices,
        default=ScoreChoice.TERRIBLE)

    class Meta(BaseReviewsComments.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            ),
        ]


class Comment(BaseReviewsComments):
    """Модель комментария для отзыва."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta(BaseReviewsComments.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
