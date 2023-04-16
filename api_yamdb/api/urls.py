from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import CategoryViewSet, TitleViewSet, CommentViewSet, ReviewViewSet

app_name = 'api'
router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register('title', TitleViewSet, basename='title')
router.register('category', CategoryViewSet, basename='category')


urlpatterns = [
    path('v1/', include(router.urls)),
]

