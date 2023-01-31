from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdmin
from .serializers import UserSerializer
from reviews.models import User


class UserViewSet(ModelViewSet):
    """Вьюсет для работы с моделью User (пользователь)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )


@api_view(["POST"])
@permission_classes([permissions.AllowAny, ])
def signup(request):
    """Регистрация нового пользователя."""
    pass


@api_view(["POST"])
@permission_classes([permissions.AllowAny, ])
def get_jwt_token(request):
    """Получение JWT-токена."""
    pass
