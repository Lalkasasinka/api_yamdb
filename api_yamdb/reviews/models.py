from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField('название', max_length=100)
    slug = models.SlugField('слаг жанра', unique=True,) 

    def __str__(self):
        return f'{self.name}'

    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField('название', max_length=100)
    slug = models.SlugField('слаг жанра', unique=True) 

    def __str__(self):
        return f'{self.name}'
    
    class Meta: 
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name= models.CharField('название', max_length=100)
    year = models.IntegerField('год')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='title', verbose_name='категория', null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='title', verbose_name='жанр')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    CHOICES = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    ]
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.OneToOneField(

    )
    text = models.TextField()
    score = models.CharField(choices=CHOICES)
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