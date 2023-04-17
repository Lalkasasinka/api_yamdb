from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import (Category, Comment, Genre, Review, Title,
                            User, NAME_LIMIT, EMAIL_LIMIT)
from .validators import validate_username

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[validate_username,
                    UniqueValidator(queryset=User.objects.all())
                    ],
                    max_lenght=NAME_LIMIT
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'role')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_lenght=NAME_LIMIT, validators=[validate_username],
        )
    confirmation_code = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_LIMIT,)
    username = serializers.CharField(
        validators=[validate_username], max_length=NAME_LIMIT)


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'
