from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken


from .filters import TitleFilter
from .mixins import CLDViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, SignUpSerializer,
                          TitleCreateSerializer, TitleReadOnlySerializer,
                          TokenSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User


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
            user, created = User.objects.get_or_create(
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
def user_profile(request) -> Response:
    """Персональная страница пользователя."""
    current_user: User = request.user
    if request.method == 'PATCH':
        serializer = UserSerializer(
            current_user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=current_user.role)
    serializer = UserSerializer(current_user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewsSet(CLDViewSet):
    """Вьюсет для работы с моделью Category (Категория)."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class GenreViewsSet(CLDViewSet):
    """Вьюсет для работы с моделью Genre (Жанр)."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class TitleCreateViewsSet(ModelViewSet):
    """Вьюсет для работы с моделью Title (Произведение)."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleCreateSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', ):
            return TitleReadOnlySerializer
        return TitleCreateSerializer


class ReviewViewSet(ModelViewSet):
    """Класс представления ревью."""

    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_title_obj(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_obj().reviews.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(
                title=self.get_title_obj(),
                author=self.request.user,
            )


class CommentViewSet(ModelViewSet):
    """Класс представления комментариев."""

    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_review_obj(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review_obj().comments.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(
                review=self.get_review_obj(),
                author=self.request.user,
            )
