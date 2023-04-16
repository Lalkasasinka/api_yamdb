from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TitleViewSet

router = DefaultRouter()
router.register('title', TitleViewSet)
router.register('category', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]