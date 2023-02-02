import re

from rest_framework import serializers


class CorrectUsernameValidator:
    """Проверка на корректное имя для пользователя."""

    RE_PATTERN: str = r'^[\w.@+-]+$'
    message = 'Не больше 150 символов: буквы, цифры и знаки "@.+-_" only.'
    requires_context = True

    def __init__(self, fields, message=None):
        self.fields = fields
        self.message = message or self.message


    def __call__(self, attrs, serializer):
        regexp = re.compile(self.RE_PATTERN)
        if regexp.search(attrs.get('username')) == None: 
            raise serializers.ValidationError(self.message)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} '
            f'(model_fields={self.fields}, '
            f'message={self.message})>'
        )
