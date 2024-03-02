# Тестовое задание Backend/Django
## Описание
Тестовое задание для HardQode для стажировки. Представляет собой простое API для системсы обучения.

## Структура проекта
В проекте реализованы следущие модели:
1. Продукт:
   + Название продукта
   + Автор продукта
   + Дата старта продукта
   + Стоимость продукта
   + Ученики продукта
2. Урок(принадлежит продукту):
   + Название урока
   + Ссылка на видео
   + Продукт, которому принадлежит урок
3. Группа(принадлежит продукту):
   + Название
   + Минимальное кол-во участников
   + Максимальное кол-во участников
   + Учасники
   + Продукт, которому принадлежит группа

## Реализованные API реквесты

### JWT Token

#### Get token

Доступ через POST реквест: ```/api/token```

Возвращает токен для доступа и рефреша

#### Refresh token

Доступ через POST реквест: ```/api/token/refresh```

Обновляет токен

#### Verify token

Доступ через POST реквест: ```/api/token/verify```

Верифицирует токен

### DataBase access

#### Get_list_of_available_products

Возвращает список продуктов, доступных пользователю для покупки в формате

``` json
{
    "id": "product.id",
    "name": "product.name",
    "price": "product.price",
    "lessons_quantity": "quantity_of_lessons",
    "author_id": "product.author_id"
}
```
Доступ через GET реквест: ```/api/products```

Требует аутентификации через JWT токен 

#### Add_product_to_the_products

Добавляет продукт в базу данных 

Доступ через POST реквест: ```/api/products```

Требует аутентификации через JWT токен

Необходимо указать следущии поля в теле запроса:
+ product_name - Название продукта
+ product_start_time - Время продукта в формате(YYYY-MM_DD hh:mm:ss)
+ product_price - Цена продукта
+ product_author_id - Id автора из существующих юзеров

#### Get_lessons_for_product
Возвращает список уроков по конкретному продукту, к которому пользователь имеет доступ

Доступ через GET реквест: ```/api/products/lessons```

Требует аутентификации через JWT токен

Необходимо указать в параметрах запроса product_id

Урок представлен в формате

```json
{
    "id": "lesson.id",
    "name": "lesson.name",
    "link_to_video": "lesson.link_to_video"
}
```
#### Get_quantity_of_students

Возвращает кол-во учеников, принадлежащих проекту

Доступ через GET реквест: ```/api/products/quantity_of_students```

Необходимо указать в параметрах запроса product_id

#### Get_percent_of_fullness_per_group
Возвращает список групп в формате
``` json
{
    "id": "group.id",
    "name": "group.name",
    "percent_of_fullness": "group.percent_of_fullness()"
}
```

Где ```group.percent_of_fullness()``` это процент заполненности группы.

Доступ через GET реквест: ```/api/products/buying_rating```

Необходимо указать в параметрах запроса product_id

#### Get_product_buying_rating

Возвращает процент приобретения продукта в формате
```json
{
    "id": "product.id",
    "name": "product.name",
    "author": "product.author_id",
    "price": "product.price",
    "product_buying_rating": "product.buying_rating()"
}
```

#### StudentAPI

##### post request(добавить студента в продукт)
Доступ через POST реквест: ```/api/student```

Требует аутентификации через JWT токен

Необходимо указать в теле запроса product_id

##### delete request(удалить студента из проекта)
Доступ через DELETE реквест: ```/api/student```

Требует аутентификации через JWT токен

Необходимо указать в теле запроса product_id
