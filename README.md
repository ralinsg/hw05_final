
# Проект hw05_final

Проект hw05_final является социальной сетью для публикации личных записей с возможностью публикацией и комментированием постов, а также подписок на авторов.


## Технологический стек:

- Python 3
- HTML
- Django
- Django ORM
- SQL
- Git
- Unittest
- Pytest
- Pillow

## Запуск проекта в dev-режиме:

Инструкция для  операционной системы windows и утилиты git bash.

Клонировать репозиторий и перейти в него в командной строке:

``` bash
 git clone git@github.com:ralinsg/hw05_final.git
```

``` bash
 cd hw05_final
```

Cоздать и активировать виртуальное окружение:

``` bash
 py -3.7 -m venv venv
```

``` bash
 source venv/Scripts/activate
```

``` bash
 python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

``` bash
 pip install -r requirements.txt
```

Выполнить миграции:

``` bash
 python manage.py makemigrations
```

``` bash
 python manage.py migrate
```

Создаем суперпользователя:

``` bash
 python manage.py createsuperuser
```

Собираем статику:

``` bash
 python manage.py collectstatic
```

Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env

``` bash
SECRET_KEY='secret_key'
```

Запускаем проект:

``` bash
 python manage.py runserver
```

После чего проект будет доступен по адресу http://localhost/

## Примеры запросов:

Отображение постов и публикаций (GET, POST)

```bash
http://127.0.0.1:8000/posts/
```

Получение, изменение, удаление поста с соответствующим id (GET, PUT, PATCH, DELETE)

```bash
http://127.0.0.1:8000/posts/{id}/
```

Получение информации о подписках текущего пользователя, создание новой подписки на пользователя (GET, POST)
 
 ```bash
http://127.0.0.1:8000/posts/follow/
```

## Авторы

- Ралин Сергей [@ralinsg](https://github.com/ralinsg)

