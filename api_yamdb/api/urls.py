from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet

v1_router = DefaultRouter
v1_router.register('reviews', ReviewViewSet, basename='reviews')
v1_router.register('comments', CommentViewSet, basename='comments')
