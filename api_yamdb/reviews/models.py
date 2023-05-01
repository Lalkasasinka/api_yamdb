from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

EMAIL_LIMIT = 254
NAME_LIMIT = 150
ROLE_LIMIT = 50
TITLE_LIMIT = 100
SLUG_LIMIT = 50
MAX_VALUE_SCORE = 10
MIN_VALUE_SCORE = 1


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=EMAIL_LIMIT,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=NAME_LIMIT,
        unique=True,
        validators=[UnicodeUsernameValidator()],
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=ROLE_LIMIT,
        choices=ROLES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    slug = models.SlugField('слаг жанра', unique=True, max_length=SLUG_LIMIT)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    slug = models.SlugField('слаг жанра', unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    year = models.PositiveIntegerField('год', db_index=True)
    description = models.TextField('описание', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='title',
        verbose_name='категория', null=True,
    )
    genre = models.ManyToManyField(Genre, related_name='title',
                                   verbose_name='жанр')

    class Meta:
        ordering = ['year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', verbose_name='Обзор'
    )

    text = models.TextField(verbose_name='Текст отзыва')
    score = models.IntegerField(
        validators=(
            MaxValueValidator(MAX_VALUE_SCORE),
            MinValueValidator(MIN_VALUE_SCORE)
        ),
        error_messages={'validators': 'Оценка должна быть от 1 до 10'},
        verbose_name='Рейтинг произведения'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )
        ]
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return self.text
