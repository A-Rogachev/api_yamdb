from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer
from reviews.models import User


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с моделью User (пользователь)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )


@api_view(["POST"])
@permission_classes([permissions.AllowAny, ])
def signup(request) -> Response:
    """Регистрация нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        username: str = serializer.validated_data['username']
        email: str = serializer.validated_data['email']

        if User.objects.filter(username=username).exists():
            return Response(
                "Пользователь с таким именем уже существует!",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            new_user: User = User.objects.create_user(
                username=username,
                email=email,
            )
        except IntegrityError:
            return Response(
                "Нельзя использовать данный электронный адрес!",
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirm_code: str = default_token_generator.make_token(new_user)
        send_mail(
            'YaMDb → подтверждение регистрации.',
            f'Код для подтверждения регистрации: {confirm_code}',
            'yamdb_service@ya.ru',
            [new_user.email, ],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny, ])
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
                {
                    'token': new_token,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            'Ошибка кода подтвеждения. Попробуйте еще раз.',
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
