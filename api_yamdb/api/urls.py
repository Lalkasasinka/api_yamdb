from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, api_get_token,
                    api_signup)

app_name = 'api'
router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('users', UserViewSet, basename='users')

auth = [
    path('signup/', api_signup),
    path('token/', api_get_token),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth))
]
