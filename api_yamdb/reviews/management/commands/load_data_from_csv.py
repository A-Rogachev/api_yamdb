import os

import pandas
from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


DATA_DIRECTORY = settings.DATA_FILE_PATH
os.chdir(DATA_DIRECTORY)

class Command(BaseCommand):
    help = 'Загружает файлы csv в базу данных.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):

        # df = pandas.read_csv('category.csv')
        # for ID, NAME, SLUG in zip(
        #         df.id,
        #         df.name,
        #         df.slug):
        #     models = Category(
        #         id=ID,
        #         name=NAME,
        #         slug=SLUG)
        #     models.save()

        # df = pandas.read_csv('genre.csv')
        # for ID, NAME, SLUG in zip(
        #         df.id,
        #         df.name,
        #         df.slug):
        #     models = Genre(id=ID, name=NAME, slug=SLUG)
        #     models.save()

        # df = pandas.read_csv('users.csv')
        # for ID, USERNAME, EMAIL, ROLE, BIO, FIRST_NAME, LAST_NAME in zip(
        #     df.id,
        #     df.username,
        #     df.email,
        #     df.role,
        #     df.bio,
        #     df.first_name,
        #     df.last_name
        # ):
        #     models = User(
        #         id=ID,
        #         username=USERNAME,
        #         email=EMAIL,
        #         role=ROLE,
        #         bio=BIO,
        #         first_name=FIRST_NAME,
        #         last_name=LAST_NAME,
        #     )
        #     models.save()

        # df = pandas.read_csv('titles.csv')
        # for ID, YEAR, NAME, CATEGORY in zip(
        #         df.id,
        #         df.year,
        #         df.name,
        #         df.category):
        #     models = Title(
        #         id=ID,
        #         year=YEAR,
        #         name=NAME,
        #         category=Category.objects.get(pk=CATEGORY),
        #     )
        #     models.save()


        df = pandas.read_csv('review.csv', quotechar='"', doublequote=True)

        # print(df)
        for ID, TITLE_ID, TEXT, AUTHOR, SCORE, PUB_DATE in zip(
            df.id,
            df.title_id,
            df.text,
            df.author,
            df.score,
            df.pub_date
        ):
            models = Review(
                id=ID,
                title_id=Title.objects.get(pk=TITLE_ID),
                text=TEXT,
                author=User.objects.get(pk=AUTHOR),
                score=SCORE,
                pub_date=PUB_DATE
            )
            models.save()





        # df = pandas.read_csv(r'static/data/comments.csv')
        # for ID, REVIEW_ID, TEXT, AUTHOR, PUB_DATE in zip(
        #     df.id,
        #     df.review_id,
        #     df.text,
        #     df.author,
        #     df.pub_date
        # ):
        #     models = Comment(
        #         id=ID,
        #         review_id=REVIEW_ID,
        #         text=TEXT,
        #         author=AUTHOR,
        #         pub_date=PUB_DATE)

            
