from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


EMAIL_LIMIT = 254
NAME_LIMIT = 150
ROLE_LIMIT = 50
TITLE_LIMIT = 100
SLUG_LIMIT = 50


class User(AbstractUser):
    Admin = 'admin'
    Moderator = 'moderator'
    User = 'user'
    Roles = [
        (Admin, 'Administrator'),
        (Moderator, 'Moderator'),
        (User, 'User'),
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
        choices=Roles,
        default=User,
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
        return self.role == self.Admin

    @property
    def is_moderator(self):
        return self.role == self.Moderator


class Category(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    slug = models.SlugField('слаг жанра', unique=True, max_length=SLUG_LIMIT)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    slug = models.SlugField('слаг жанра', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    year = models.IntegerField('год')
    description = models.TextField('описание', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='title',
        verbose_name='категория', null=True,
    )
    genre = models.ManyToManyField(Genre, related_name='title',
                                   verbose_name='жанр')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                                 related_name='reviews', verbose_name='обзор')
    text = models.TextField()
    score = models.IntegerField(
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1)
        ),
        error_messages={'validators': 'Оценка должна быть от 1 до 10'}
    )
    created_time = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )
        ]
        ordering = ('created_time',)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    Reviews = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created_time = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
