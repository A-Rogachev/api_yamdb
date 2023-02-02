from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, get_jwt_token, signup,
                    ReviewViewSet, CommentViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('reviews', ReviewViewSet, basename='reviews')
v1_router.register('comments', CommentViewSet, basename='comments')


urlpatterns = (
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='get_jwt_token'),
    path('v1/', include(v1_router.urls)),
)
