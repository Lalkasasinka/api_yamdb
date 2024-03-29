from django.contrib import admin

from .models import Category, Genre, Title, User

admin.site.register(User)


@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    ...


@admin.register(Title)
class GroupAdmin(admin.ModelAdmin):
    ...


@admin.register(Genre)
class GroupAdmin(admin.ModelAdmin):
    ...
