from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Модель категории произведения."""

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
        """Строковое представления категории."""
        return self.name


class Genre(models.Model):
    """Модель жанра произведения."""

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
        """Строковое представления жанра."""
        return self.name


class Title(models.Model):
    """Модель произведения."""

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


class Review(models.Model):
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

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews",
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews",
    )
    score = models.IntegerField(
        choices=ScoreChoice.choices,
        default=ScoreChoice.TERRIBLE,
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            ),
        ]


class Comment(models.Model):
    """Модель комментария для отзыва."""

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments",
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True,
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments",
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
