# Generated by Django 3.2 on 2023-04-22 12:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_user_bio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('created_time',)},
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(error_messages={'validators': 'Оценка должна быть от 1 до 10'}, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='обзор'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique review'),
        ),
    ]