from rest_framework import mixins, viewsets


class CLDViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """Вьюсет, исключающий использование методов create, update."""

    pass
