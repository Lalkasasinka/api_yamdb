import datetime as dt
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import (EMAIL_LIMIT, NAME_LIMIT, Category, Comment, Genre,
                            Review, Title, User)

from .validators import validate_username
from reviews.models import MAX_VALUE_SCORE, MIN_VALUE_SCORE


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())
                    ], max_length=NAME_LIMIT)

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=NAME_LIMIT, validators=[validate_username],)
    confirmation_code = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_LIMIT,)
    username = serializers.CharField(
        validators=[validate_username], max_length=NAME_LIMIT)


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'review', 'author', 'pub_date',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(slug_field='name', read_only=True)
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate_score(self, value):
        if MIN_VALUE_SCORE > value and value > MAX_VALUE_SCORE:
            raise serializers.ValidationError('Оценка должна быть от 1 до 10')
        return value

    def validate(self, data):
        request = data['request']
        author = request.user
        if (
            request.method == "POST"
            and Review.objects.filter(
                title=self.context.get('view').kwargs.get('title_id'),
                author=author
            ).exists()
        ):
            raise serializers.ValidationError('Один пользователь - один отзыв')
        return data
    


    class Meta:
        fields = '__all__'
        model = Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    def validate_year(self, value):
        now = dt.datetime.now().year
        if value > now:
            raise serializers.ValidationError(
                f'{value} не может быть больше {now}'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
