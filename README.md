## Проект YaMDb

YaMDb - API-сервис для публикации отзывов пользователей на различные произведения.

### Как запустить проект:

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

### Примеры запросов:

Получить список всех публикаций:
```
GET http://127.0.0.1:8000/api/v1/posts/

{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "anton",
            "text": "Первый пост",
            "pub_date": "2022-05-25T16:42:52.721570Z",
            "image": null,
            "group": 2
        },
        ...
        {
            "id": 5,
            "author": "anton",
            "text": "Пятый пост",
            "pub_date": "2022-05-26T11:25:40.045193Z",
            "image": null,
            "group": null
        }
    ]
}
```