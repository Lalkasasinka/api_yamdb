from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from production.models import Review
from .serializers import CommentSerializer, ReviewSerializer


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
