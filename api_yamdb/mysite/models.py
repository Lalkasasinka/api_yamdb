from django.contrib.auth import get_user_model
from django.db import models


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
    genre = models.ManyToManyField(Genre, related_name='title', verbose_name='жанр', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
