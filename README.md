<a id='start_page'></a>
# <p align = center>API для проекта YaMDB</p>
#### *Проект **YaMDb** собирает отзывы пользователей на различные произведения.*
___

- Любой пользователь может просматривать описания произведений, читать отзывы и комментарии.
-   Аутентифицированный пользователь может читать/публиковать отзывы и ставить оценки произведениям; комментировать чужие отзывы, редактировать и удалять свои отзывы и комментарии.
- Авторизованный пользователь может редактировать данные своей учетной записи.
- Любой пользователь может зарегистрироваться на сервисе (используется адрес электронной почты). 

  [![](https://img.shields.io/badge/Python-3.7.9-blue)](https://www.python.org/downloads/release/python-379/) [![](https://img.shields.io/badge/Django-3.2.16-green)](https://docs.djangoproject.com/en/4.1/releases/3.2.16/) [![](https://img.shields.io/badge/DRF-3.2.14-orange)](https://www.django-rest-framework.org/community/release-notes/#3124)

#### Как запустить проект:
1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/A-Rogachev/api_yamdb.git
```
```
cd api_yamdb
```
2. Создать и активировать виртуальное окружение.
```
python3 -m venv env
```
```
source env/bin/activate
```
3. Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
4. Выполнить миграции:
```
python3 manage.py migrate
```
5. Запустить проект:
 ```
python3 manage.py runserver
```
#### *Документацию проекта, а также примеры запросов к API можно найти по следующему URL после запуска проекта:*
```
http://127.0.0.1:8000/redoc/
```

#### Авторы

><font size=2>Зименко Михаил / Рогачев Александр / Шамраев Андрей
>Студенты факультета Бэкенд. Когорта № 50</font>

[наверх](#start_page)