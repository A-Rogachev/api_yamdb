from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from rest_framework.validators import UniqueTogetherValidator

from .validators import CorrectUsernameValidator
from reviews.models import LIMIT_USERNAME_LENGTH, Comment, Review, Title, User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=['user', 'title'],
                message='Вы уже оставляли отзыв.',
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


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


class UserProfileSerializer(UserSerializer):
    """Сериализатор для личной страницы пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role', )


class SignUpSerializer(serializers.Serializer):
    """Регистрация нового пользователя."""

    username = CharField(max_length=LIMIT_USERNAME_LENGTH, required=True)
    email = EmailField(max_length=254, required=True)

    validators = [
        CorrectUsernameValidator(
            username_field='username',
            forbidden_names=['me', 'Me']
        ),
    ]


class TokenSerializer(serializers.Serializer):
    """Получение JWT-токена в обмен на username и confirmation code."""

    username = CharField(max_length=LIMIT_USERNAME_LENGTH, required=True)
    confirmation_code = CharField(required=True)
