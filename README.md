![](https://img.shields.io/badge/Python-3.7.0-blue) 
![](https://img.shields.io/badge/Django-2.2.16-orange)
![](https://img.shields.io/badge/DjangoRestFramework-3.12.4-red)
<br>

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