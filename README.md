#Проект «Проект YaMDb».
---
### Описание

API для YaMDb представляет собой проект, который собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

---
Стек технологий
---

- Python 3.11,
- Django 4.2,
- DRF,
- JWT + Djoser

---
##Запуск проекта в dev-режиме
 Клонировать репозиторий и перейти в него в командной строке.
- Установите и активируйте виртуальное окружение c учетом версии Python 3.7 (выбираем python не ниже 3.7):
```
python -m venv venv
```
```
source venv/Scripts/activate
```
- Устанавливаем зависимости из файла __requirements.txt__
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
- Выполянем миграции
```
python manage.py migrate
```
- Создаем суперпользователя:
```
python manage.py createsuperuser
```
- Запускаем проект:
```
python manage.py runserver
```
---
##Примеры работы с API для всех пользователей

###Регистрация
```
POST api/v1/auth/signup/ - Получить код подтверждения на переданный email
POST api/v1/auth/token/ - Получение JWT-токена в обмен на username и confirmation code
```
Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится.
```
GET api/v1/titles/ - получить список всех произведений.
GET api/v1/titles/{id}/ - получение произведения по id.
GET api/v1/genre/ - получение списка жанров.
GET api/v1/categories/ - получение списка категорий.
GET api/v1/titles/{titles_id}/reviews/ - получить список всех отзывов
GET api/v1/titles/{titles_id}/reviews/{reviews_id} - получить отзыв
GET api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получить список всех комментариев к отзыву по id
GET api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - Получить комментарий для отзыва по id
```
---
##Примеры работы с API для авторизованных пользователей

```
POST api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Добавить новый комментарий для отзыва
POST api/v1/titles/{title_id}/reviews/ - Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение
```
---
Авторы в telegram: 
- [Иван](https://t.me/sSinichka)
- [Рома](https://t.me/RomaMaklakov)
- [Данил](https://t.me/daniil_mihaylov)
