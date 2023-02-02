from rest_framework import mixins, viewsets
from django.views.generic import DetailView
from recipes.models import Recipe
from django.shortcuts import get_object_or_404

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
