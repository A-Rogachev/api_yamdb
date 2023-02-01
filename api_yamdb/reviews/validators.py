from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    """Проверка валидности года выпуска произведения. 
    Если пользователь ввел год который еще 
    не наступил, поднимается исключение."""
    dt_now = datetime.now()
    if year > dt_now.year:
        raise ValidationError(f'Неверно указан год выпуска')
