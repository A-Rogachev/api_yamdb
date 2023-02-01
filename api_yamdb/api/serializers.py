from rest_framework import serializers
from reviews.models import Title, Review, Comment
from rest_framework.validators import UniqueTogetherValidator


class ReviewsSerializer(serializers.ModelSerializer):
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
