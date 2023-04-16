from rest_framework import filters, mixins, permissions, viewsets

from reviews.models import Category, Genre, Title
from .serializers import TitleSerializer, CategorySerializer


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
