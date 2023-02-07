import csv
import os
import sys
from typing import Dict

from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.db.models import Model

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

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
            try:
                with open(
                    file_and_args[0], 'r', encoding='utf-8'
                ) as data_file:
                    objects_queue = []
                    reader = csv.DictReader(
                        data_file,
                        delimiter=',',
                        quotechar='"',
                        skipinitialspace=True,
                    )
                    for row in reader:
                        data_args: Dict[str, str] = dict(**row)
                        if file_and_args[1]:
                            for key, value in file_and_args[1].items():
                                data_args[key] = value.objects.get(
                                    pk=data_args[key]
                                )
                        objects_queue.append(db_model(**data_args))
                    db_model.objects.bulk_create(objects_queue)

            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR(
                        f'Файла {file_and_args[0]} нет в рабочем каталоге!'
                        '\nРабота загрузчика прервана!'
                    )
                )
                sys.exit()
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(
                        f'Oшибка при работе с файлом{file_and_args[0]}'
                        '\nРабота загрузчика прервана!'
                    )
                )
                sys.exit()
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные из файла {file_and_args[0]} успешно загружены'
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                'Работа загрузчика завершена успешно!'
            )
        )
