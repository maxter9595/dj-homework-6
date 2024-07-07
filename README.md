# Алгоритм запуска проекта

1. Настройте виртуальное окружение и подключитесь к нему:
   - ``venv\Scripts\activate`` - для Windows
   - ``source venv/bin/activate`` - для MacOS и Linux
```bash
python -m venv venv
venv\Scripts\activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Убедитесь, что в settings.py правильно указаны параметры для подключения к базе данных (БД):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netology_stocks_products',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}
```

4. Создайте БД с именем, указанным в NAME (netology_smart_home):
```bash
createdb -U postgres netology_smart_home
```

5. Осуществите команды для создания миграций приложения с БД:
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Запустите приложение:
```bash
python manage.py runserver
```

7. Откройте ``requests-examples.http`` в VS Code (REST Client) и реализуйте запросы.

# Реализация запросов (на примере REST Client из VS Code)

- Примеры реализации запросов представлены в файле ``requests-examples.http``

- Создание продукта/продуктов:
```http
@baseUrl = http://localhost:8000/api

POST {{baseUrl}}/products/
Content-Type: application/json

{
  "products": [
    {
      "title": "Помидор",
      "description": "Самые сочные и ароматные помидорки"	
    },
    {
      "title": "Огурец",
      "description": "Лучшие огурцы на рынке"
    },
    {
      "title": "Морковка",
      "description": "Лучшие морковки на рынке"
    }
  ]
}
```

- Получение продуктов:
```http
GET {{baseUrl}}/products/
Content-Type: application/json
```

- Поиск продуктов по названию и описанию:
```http
GET {{baseUrl}}/products/?search=помидор
Content-Type: application/json
```

- Обновление продукта
```http
PATCH {{baseUrl}}/products/1/
Content-Type: application/json

{
  "description": "Самые сочные и ароматные помидорки"
}
```

- Удаление продукта
```http
DELETE {{baseUrl}}/products/1/
Content-Type: application/json
```

- Создание склада
```http
POST {{baseUrl}}/stocks/
Content-Type: application/json

{
  "address": "мой адрес не дом и не улица, мой адрес сегодня такой: www.ленинград-спб.ru3",
  "positions": [
    {
      "product": 2,
      "quantity": 250,
      "price": 120.50
    },
    {
      "product": 3,
      "quantity": 100,
      "price": 180
    }
  ]
}
```

- Обновляем записи на складе
```http
PATCH {{baseUrl}}/stocks/1/
Content-Type: application/json

{
  "positions": [
    {
      "product": 2,
      "quantity": 100,
      "price": 130.80
    },
    {
      "product": 3,
      "quantity": 243,
      "price": 145
    }
  ]
}
```

- Поиск складов, где есть определенный продукт (по ID продукта)
```http
GET {{baseUrl}}/stocks/?products=3
Content-Type: application/json
```

- Поиск складов, где есть определенный продукт (по названию и описанию)
```http
GET {{baseUrl}}/stocks/?search=огур
Content-Type: application/json
```

# Текст задания ("Склады и товары")

## Техническая задача: реализовать CRUD-логику для продуктов и складов, используя Django Rest Framework.

**CRUD** — аббревиатура для Create-Read-Update-Delete. Ей обозначают логику для операций создания-чтения-обновления-удаления сущностей. Подробнее: https://ru.wikipedia.org/wiki/CRUD.

## Описание

У нас есть продукты, которыми торгует компания. Продукты описываются названием и необязательным описанием (см. `models.py`). Также компания имеет ряд складов, на которых эти продукты хранятся. У продукта на складе есть стоимость хранения, поэтому один и тот же продукт может иметь разные стоимости на разных складах.

Необходимо реализовать REST API для создания, получения, обновления, удаления продуктов и складов. Так как склады имеют информацию о своих продуктах через связанную таблицу, необходимо переопределить методы создания и обновления объектов в сериализаторе (см. `serializers.py`).

Помимо CRUD-операций, необходимо реализовать поиск продуктов по названиям и описанию. И поиск складов, в которых есть определенный продукт, по идентификатору. Подробности в файле `requests-examples.http`.

Так как продуктов и складов может быть много, то необходимо реализовать пагинацию для вывода списков.

Рекомендуется обратить внимание на реализацию файлов `urls.py`. Менять их не надо, просто обратить внимание и осознать.

## Подсказки

1. Вам необходимо будет задать логику во views и serializers. В места, где нужно добавлять код, включены комментарии. После того, как вы добавите код, комментарии можно удалить.

2. Для обновления объектов удобно использовать метод `update_or_create`: https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update-or-create.

## Дополнительное задание

### Поиск складов с продуктами

Реализуйте поиск складов, в которых есть определённый продукт, но при этом указывать хочется не идентификатор продукта, а название, его часть или часть описания.

Пример запроса:

```
# поиск складов, где есть определенный продукт
GET {{baseUrl}}/stocks/?search=помид
Content-Type: application/json
```

## Документация по проекту

Для запуска проекта необходимо

Установить зависимости:

```bash
pip install -r requirements.txt
```

Вам необходимо будет создать базу в postgres и прогнать миграции:

```base
manage.py migrate
```

Выполнить команду:

```bash
python manage.py runserver
```
