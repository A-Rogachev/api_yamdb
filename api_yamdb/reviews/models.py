from django.db import models

from .validators import validate_year


class Categories(models.Model):
    """Модель категории один к одному"""
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг категории',
        max_length=50,
        unique=True
    )

class Genres(models.Model):
    """Модель жанры один ко многим"""
    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг жанра',
        max_length=50,
        unique=True
    )

class Titles(models.Model):
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
    ganre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name = 'titles',
        null=True
    )
    category = models.OneToOneField(
        Categories,
        on_delete=models.SET_NULL,
        related_name = 'titles',
        null=True
    )
