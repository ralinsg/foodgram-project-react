from rest_framework import mixins, viewsets


class ListRetrieveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Возвращает список объектов.
    Возвращает объект.
    """
    pass

class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Создает объект.
    Возвращает список объектов.
    Удаляет объект.
    """
    pass

class CreateListDestroyRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Создает объект.
    Возвращает список объектов.
    Удаляет объект.
    Возвращает объект.
    """
    pass
