from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Title(models.Model):
    pass


class Review(models.Model):

    class ScoreChoice(models.IntegerChoices):
        TERRIBLE = 1
        WILDLY = 2
        NIGHTMATE = 3
        BLOODCURDLING = 4
        POORLY = 5
        NO_BAD = 6
        FINE = 7
        GOOD = 8
        GREAT = 9
        PERFECT = 10

    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.IntegerField(choices=ScoreChoice.choices)
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


# Вот здесь, наверно, можно проверить, что автор уже оставлял отзыв к title
# Еще есть вариант проверки в сериализаторе. Кажется, оба должны работать.
# Как думаете как лучше?

    # class Meta:
    #     constraints = (
    #         models.UniqueConstraint(
    #             fields=(
    #                 "title",
    #                 "author",
    #             ),
    #             name="unique_review",
    #         ),
    #     )


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
