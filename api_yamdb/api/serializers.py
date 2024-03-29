from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField

from .validators import CorrectUsernameValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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

    username = CharField(
        max_length=settings.LIMIT_USERNAME_LENGTH,
        required=True,
    )
    email = EmailField(
        max_length=settings.LIMIT_USER_EMAIL_LENGTH,
        required=True,
    )

    validators = [
        CorrectUsernameValidator(
            username_field='username',
            forbidden_names=['me', 'Me', 'ME', 'mE'],
            ignore_case=False,
        ),
    ]


class TokenSerializer(serializers.Serializer):
    """Получение JWT-токена в обмен на username и confirmation code."""

    username = CharField(
        max_length=settings.LIMIT_USERNAME_LENGTH,
        required=True,
    )
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
    rating = serializers.IntegerField(read_only=True)

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
        queryset=Category.objects.all(),
    )

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
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


class ReviewsSerializer(serializers.ModelSerializer):
    """Класс сериализатора ревью."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        title: str = self.context['view'].kwargs.get('title_id')
        author: str = self.context['view'].request.user
        if (
            Review.objects.filter(title=title, author=author).exists()
            and self.context['view'].request.method == 'POST'
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв!')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Класс сериализатора комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('review', 'author')
