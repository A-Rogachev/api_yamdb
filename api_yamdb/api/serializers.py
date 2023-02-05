from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import (LIMIT_USERNAME_LENGTH, Category, Comment, Genre,
                            Review, Title, User)
from reviews.validators import validate_year

from .validators import CorrectUsernameValidator


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


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title. Получение информации о произведении."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(
        read_only=True
    )
    # year = serializers.IntegerField(
    #     validators=(validate_year,)
    # )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title. Создание записи о произведении."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


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
