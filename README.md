api_final
Автор:
Андрей Шамраев

Описание:
api final - это REST API для блог-платформы Yatube. Позволяет просматривать и отправлять посты, просматривать группы, подписываться на авторов.

Как запустить проект:
Ссылка на репозиторий: https://github.com/AnShamraev/api_yatube
Клонируйте репозиторий в командной строке:

git clone https://github.com/AnShamraev/api_yatube

Cоздать и активировать виртуальное окружение:

python -m venv venv
.venv/Scripts/activate 
Установить зависимости из файла requirements.txt:

python -m pip install --upgrade pip
pip install -r requirements.txt
Выполнить миграции:

python manage.py migrate
Запустить проект:

python manage.py runserver
Примеры запросов:
Запрос JWT токена с использованием логина и пароля пользователя User1:
  [POST].../api/v1/jwt/create/
  {
    "username": "User1",
    "password": "P@ssw0rd1"
}
Ответ:
{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MjA5NTYwNywianRpIjoiMDBmMGI0MG.sE5Bd3vrnQLIAL5GxxFg36tPoYyB9I5MQBE_iGshpK4",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyMDk1NjA3LCJqdGkiOiI0YmIxN2MzODcwNGU0YzQ0OWQ4Nzg4NzA4ODcyZTliMCIsInVzZXJfaWQiOjF9"
}
Запрос с использованием токена пользователя User1 для публикации поста:
    [POST].../api/v1/posts/
    {
    "text": "Test text1",
    "group": 1   
    }
Ответ:
{
    "id": 2,
    "text": "Test text1",
    "author": "User1",
    "image": null,
    "group": 1,
    "pub_date": "2023-01-27T16:05:15.321412Z"
}
Запрос для просмотра групп анонимным пользователем:
    [GET].../api/v1/groups/
Пример ответа:
    [
  {
    "id": 1,
    "title": "Group 1",
    "slug": "Group1",
    "description": "The first group"
  },
  {
    "id": 2,
    "title": "Group 2",
    "slug": "Group2",
    "description": "The second group"
  },
  {
    "id": 3,
    "title": "Group 3",
    "slug": "Grup3",
    "description": "The third group"
  }
]
Подробная документация в формате ReDoc доступна по адресу .../redoc/