from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import (viewsets, filters, mixins,
                            permissions, viewsets, status)
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework.viewsets import GenericViewSet
=======
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import AccessToken
>>>>>>> 7f982ab2d843b4c7a1c39b9f6a60ae30f6b34fe8

from reviews.models import Category, Genre, Title, Review, User
from .serializers import (TitleSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer, GenreSerializer)
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    http_method_names = ('patch', 'post', 'get', 'delete')

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(permissions.IsAuthenticated,), url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            user = request.user
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


@api_view(['POST'])
def api_get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, data['confirmation_code']):
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_201_CREATED)
    return Response(serializer.validated_data,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, _ = User.objects.get_or_create(
            **serializer.validated_data
        )
    except Exception:
        return Response(
            'Такой username или e-mail уже используется.',
            status=status.HTTP_400_BAD_REQUEST)
    code = default_token_generator.make_token(user)
    message = f'Здравствуйте, {username}! Ваш код подтверждения: {code}'
    send_mail(_, message, 'support@yamdb.com', [email])
    return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    """Список категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.DestroyModelMixin, GenericViewSet):
    """Список жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter)
    search_fields = ('=name',)
    lookup_field = 'slug'



class TitleViewSet(viewsets.ModelViewSet):
    """Список произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
