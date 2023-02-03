import re
from typing import List, Optional

from rest_framework import serializers


class CorrectUsernameValidator:
    """Проверка на корректное имя для пользователя."""

    MESSAGE_ERR_COMMON = 'Ошибка в имени пользователя'
    MESSAGE_ERR_SYMBOLS: str = (
        'Имя пользователя должно состоять из символов {}!'
    )
    MESSAGE_FORBIDDEN_NAME: str = (
        'Имя {} входит в список запрещенных для регистрации: {}'
    )

    re_pattern: str = r'^[\w.@+-]+$'
    requires_context = True

    def __init__(self,
                username_field: str,
                re_pattern: Optional[str]=None,
                forbidden_names: Optional[List[str]]=None,
                ) -> None:

        self.username_field: str = username_field
        self.re_pattern: str = re_pattern or self.re_pattern
        self.forbidden_names: Optional[List[str]] = forbidden_names

    def check_username_symbols(self, username: str) -> None:
        """Проверяем на корректные символы в имени пользователя."""
        regexp: re.Pattern = re.compile(self.re_pattern)
        if not regexp.search(username): 
            raise serializers.ValidationError(
                {
                    self.MESSAGE_ERR_COMMON:
                    f'{self.MESSAGE_ERR_SYMBOLS.format(self.re_pattern)}'
                }
            )

    def check_forbidden_names(self, username: str) -> None:
        """Проверяем на запрещенные для регистрации имена."""
        if self.forbidden_names:
            if username.lower() in [
                name.lower() for name in self.forbidden_names
            ]:
                raise serializers.ValidationError(
                    {
                        self.MESSAGE_ERR_COMMON:
                        f'{self.MESSAGE_FORBIDDEN_NAME.format(username, self.forbidden_names)}'
                    }
                )

    def __call__(self, attrs, serializer):
        new_username: str = attrs.get(self.username_field)
        self.check_username_symbols(new_username)
        self.check_forbidden_names(new_username)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__} '
            f'(username_field="{self.username_field}", '
            f're_pattern="{self.re_pattern}", '
            f'forbidden_names={self.forbidden_names})>'
        )
