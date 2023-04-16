from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import CategoryViewSet, TitleViewSet, CommentViewSet, ReviewViewSet

app_name = 'api'
router = DefaultRouter

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet)
router.register('title', TitleViewSet)
router.register('category', CategoryViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]

