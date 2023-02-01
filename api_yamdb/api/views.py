from rest_framework import permissions, viewsets
from .permissions import IsAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from .serializers import ReviewsSerializer, CommentsSerializer
from reviews.models import Reviews


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    def get_review_id(self):
        review = get_object_or_404(
            Reviews, pk=self.kwargs.get('review_id')
        )
        return review

    def get_queryset(self):
        review = self.get_review_id()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review_id()
        serializer.save(author=self.request.user, review=review)
