from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CLDViewSet
from .pagination import UsersPagination
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleCreateSerializer, TitleReadOnlySerializer,
                          TokenSerializer, UserProfileSerializer,
                          UserSerializer)


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с моделью User (пользователь)."""

    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    pagination_class = PageNumberPagination


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request) -> Response:
    """Регистрация нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username: str = serializer.validated_data['username']
        email: str = serializer.validated_data['email']
        try:
            user: User = get_object_or_404(
                User,
                username=username,
                email=email,
            )
        except Http404:
            try:
                user: User = User.objects.create_user(
                    username=username,
                    email=email,
                )
            except IntegrityError:
                return Response(
                    'Нельзя использовать данный электронный адрес!',
                    status=status.HTTP_400_BAD_REQUEST,
                )
        confirm_code: str = default_token_generator.make_token(user)
        send_mail(
            'YaMDb: подтверждение регистрации.',
            f'Код для подтверждения регистрации: {confirm_code}',
            'yamdb_service@ya.ru',
            [user.email, ],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request) -> Response:
    """Получение JWT-токена."""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username: str = serializer.validated_data['username']
        confirm_code: str = serializer.validated_data['confirmation_code']
        user: User = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirm_code):
            new_token: str = str(RefreshToken.for_user(user).access_token)
            return Response(
                {'token': new_token, },
                status=status.HTTP_200_OK,
            )
        return Response(
            'Ошибка получения кода подтверждения. Попробуйте еще раз.',
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_profile(request) -> Response:
    """Персональная страница пользователя."""
    current_user: User = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(current_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = UserProfileSerializer(
        current_user,
        data=request.data,
        partial=True,
    )
    if serializer.is_valid():
        serializer.save(role=current_user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewsSet(CLDViewSet):
    """Получить категории - без токена. Создать категорию - администратор."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class GenreViewsSet(CLDViewSet):
    """Получить жанры - без токена. Создать жанр - администратор."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class TitleCreateViewsSet(ModelViewSet):
    """Получить объекты - без токена. Создать запись - администратор."""

    queryset = Title.objects.all()
    serializer_class = TitleCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)


    def get_serializer_class(self):
        if self.action == list or self.action == 'retrieve':
            return TitleReadOnlySerializer
        return TitleCreateSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentsSerializer

    def get_review_id(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        return review

    def get_queryset(self):
        review = self.get_review_id()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review_id()
        serializer.save(author=self.request.user, review=review)
