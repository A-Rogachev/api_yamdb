from django.db import models

from .validators import validate_year


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
        through='TitleGenre',
        related_name = 'titles',
        null=True
    )
    category = models.OneToOneField(
        Category,
        on_delete=models.SET_NULL,
        related_name = 'titles',
        null=True
    )

class TitleGenre(models.Model):
        genre = models.ForeignKey(
            Genre, 
            on_delete=models.SET_NULL
        )
        title = models.ForeignKey(
            Title, 
            on_delete=models.SET_NULL
        )
