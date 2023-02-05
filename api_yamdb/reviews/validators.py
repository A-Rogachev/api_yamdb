from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    """Валидация года выпуска произведения."""
    if year > datetime.now().year:
        raise ValidationError(f'Неверно указан год выпуска: {year}')
