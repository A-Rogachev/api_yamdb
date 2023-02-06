import csv
import os
from typing import Dict

from django.conf import settings
from django.core.management import BaseCommand
from django.db.models import Model
from reviews.models import Category, Comment, Genre, Review, Title, User

DATA_DIRECTORY: str = settings.DATA_FILE_PATH
os.chdir(DATA_DIRECTORY)

data_for_database: Dict[Model, str] = {
    Category: ('category.csv', ''),
    Genre: ('genre.csv', ''),
    User: ('users.csv', ''),
    Title: ('titles.csv', {'category': Category}),
    Review: ('review.csv', {'author': User}),
    Comment: ('comments.csv', {'author': User}),
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for db_model, file_and_args in data_for_database.items():
            data_file = open(file_and_args[0], 'r', encoding='utf-8')
            objects_queue = []
            reader = csv.DictReader(
                data_file,
                delimiter=',',
                quotechar='"',
                skipinitialspace=True,
            )
            # случай, когда необходимо переопределить значения в аргументах
            if not file_and_args[1]:
                for row in reader:
                    objects_queue.append(db_model(**row))
            else:
                for row in reader:
                    data_args: Dict[str, str] = dict(**row)
                    for key, value in file_and_args[1].items():
                        data_args[key] = value.objects.get(pk=data_args[key])
                    objects_queue.append(db_model(**data_args))

            db_model.objects.bulk_create(objects_queue)
            data_file.close()
