from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


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
