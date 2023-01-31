from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import User


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


class SignUpSerializer(serializers.ModelSerializer):
    """Регистрация нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')
