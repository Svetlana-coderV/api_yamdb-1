![](https://img.shields.io/badge/Python-3.7.0-blue) 
![](https://img.shields.io/badge/Django-2.2.16-orange)
![](https://img.shields.io/badge/DjangoRestFramework-3.12.4-red)
<br>

## Проект YaMDb

**YaMDb** - API-сервис для публикации отзывов пользователей на различные произведения.
<br><br>

**Особенности:**

:black_small_square: система регистрации пользователей с JWT-токеном<br>
:black_small_square: различные пользовательские роли: аононим, аутентифицированный пользователь, модератор, администратор<br>
:black_small_square: категории и жанры произведений<br>
:black_small_square: возможность оставлять отзывы с оценками и комментарии к ним пользователями, их редактирование авторами<br><br>

## Используемые технологии:

:black_small_square: **Python**<br>
:black_small_square: **Django**<br>
:black_small_square: **Django Rest Framework**<br>
:black_small_square: **GIT**<br>
:black_small_square: **SQLite**<br><br>

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Anton-Kim/api_yamdb.git
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```

### Импорт данных из прилагаемых .csv файлов (api_yamdb/static/data/) в базу данных проекта:

**Файлы .csv должны располагаться по умолчанию в подпапке проекта static/data/, база данных должна иметь расположение и имя по умолчанию db.sqlite3**

Скачать программу SQLite и поместить ее в корневую папку проекта api_yamdb:

```
sqlite.org/download.html
```

В случае несоответствия последовательности полей в .csv файле полям таблицы, необходимо пересортировать поля в .csv файле.
Для VSCode можно воспользоваться плагином **Edit csv**:

```
marketplace.visualstudio.com/items?itemName=janisdd.vscode-edit-csv
```

В терминале bash сделать прилагаемый скрипт db_import_script.sh (располагается в той же папке, что и db.sqlite3) исполняемым следующей командой:

```
chmod +x ./db_import_script.sh
```

Запустить выполнение скрипта с указанием двух обязательных аргументов - имя файла csv (без расширения), имя модели (таблицы) в базе данных (без префикса reviews_):

```
./db_import_script.sh <имя_файла> <имя_модели>
```

Повторить выполнение скрипта для каждой пары файл-таблица.

<br>

## Процедура регистрации:

Получение кода подтверждения на переданный email:
```
POST http://127.0.0.1:8000/api/v1/auth/signup/

{
"email": "ваш email",
"username": "ваш username"
}
```
Получение JWT-токена в обмен на username и confirmation code из письма:
```
POST http://127.0.0.1:8000/api/v1/auth/token/

{
"username": "ваш username",
"confirmation_code": "confirmation code из письма"
}
```
Далее токен необходимо передавать в заголовке каждого запроса, в поле Authorization. Перед самим токеном должно стоять ключевое слово Bearer и пробел:
```
Bearer <токен>
```
<br>

## Примеры запросов:

Получение списка всех произведений:
```
GET http://127.0.0.1:8000/api/v1/titles/

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "category": {
                "name": "Музыка",
                "slug": "music"
            },
            "genre": [
                {
                    "name": "Поп-рок",
                    "slug": "pop-rock"
                }
            ],
            "rating": 6,
            "name": "A-Ha - Lifelines",
            "year": 2002,
            "description": "Песня"
        },
        {
            "id": 2,
            "category": {
                "name": "Фильмы",
                "slug": "films"
            },
            "genre": [
                {
                    "name": "Мыло",
                    "slug": "soap"
                }
            ],
            "rating": 4,
            "name": "Санта Барбара",
            "year": 1984,
            "description": ""
        }
    ]
}
```
Полуение отзыва по id:
```
GET http://127.0.0.1:8000/api/v1/titles/1/reviews/4/

{
    "id": 3,
    "author": "leo",
    "text": "Потянет",
    "score": 5,
    "pub_date": "2022-06-17T10:44:44.562182Z"
}
```
Добавление комментария к отзыву:
```
POST http://127.0.0.1:8000/api/v1/titles/1/reviews/4/comments/

{
"text": "Не могу не согласиться"
}
```
<br>

## Авторы проекта:

### Андреев Антон:
```
e-mail: obsos32@gmail.com
GitHub: github.com/Anton-Kim
```
### Ванеева Светлана:
```
e-mail: karasevalana@gmail.com
GitHub: github.com/Svetlana-coderV
```

### Гисматуллин Эрик:
```
e-mail: gismatullin1803@mail.ru
GitHub: github.com/Erik180
```
