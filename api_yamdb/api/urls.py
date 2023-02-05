from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewsSet, CommentViewSet, GenreViewsSet,
                    ReviewViewSet, TitleCreateViewsSet, UserViewSet,
                    get_jwt_token, signup, user_profile)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewsSet, basename='categories')
v1_router.register('genres', GenreViewsSet, basename='genres')
v1_router.register('titles', TitleCreateViewsSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
v1_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='get_jwt_token'),
    path('v1/users/me/', user_profile, name='user_profile'),
    path('v1/', include(v1_router.urls)),
]
