from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, permissions, viewsets

from reviews.models import Category, Genre, Title, Review
from .serializers import TitleSerializer, CategorySerializer, CommentSerializer, ReviewSerializer


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
    Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """Список категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('=name',)

class TitleViewSet(viewsets.ModelViewSet):
    """Список произведений."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer

