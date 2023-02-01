from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from reviews.models import LIMIT_USERNAME_LENGTH, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User (пользователь)."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignUpSerializer(serializers.Serializer):
    """Регистрация нового пользователя."""

    username = CharField(max_length=LIMIT_USERNAME_LENGTH, required=True)
    email = EmailField(max_length=254, required=True)


class TokenSerializer(serializers.Serializer):
    """Получение JWT-токена в обмен на username и confirmation code."""

    username = CharField(max_length=LIMIT_USERNAME_LENGTH, required=True)
    confirmation_code = CharField(required=True)
