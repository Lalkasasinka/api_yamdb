from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


EMAIL_LIMIT = 254
NAME_LIMIT = 150
ROLE_LIMIT = 50
TITLE_LIMIT = 100


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
    slug = models.SlugField('слаг жанра', unique=True,) 

    def __str__(self):
        return f'{self.name}'

    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField('название', max_length=TITLE_LIMIT)
    slug = models.SlugField('слаг жанра', unique=True) 

    def __str__(self):
        return f'{self.name}'
    
    class Meta: 
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name= models.CharField('название', max_length=TITLE_LIMIT)
    year = models.IntegerField('год')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='title', verbose_name='категория', null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='title', verbose_name='жанр')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

class Review(models.Model):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9 
    ten = 10
    CHOICES_SCORE = [
        (one, "1"),
        (two, "2"),
        (three  , "3"),
        (four, "4"),
        (five, "5"),
        (six, "6"),
        (seven, "7"),
        (eight, "8"),
        (nine, "9"),
        (ten, "10"),
    ]
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.OneToOneField(Title, on_delete=models.CASCADE, related_name='review', verbose_name='обзор')
    text = models.TextField()
    score = models.CharField(choices=CHOICES_SCORE, max_length=2)
    created_time = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

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