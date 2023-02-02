from api.filters import IngredientFilter
from api.mixins import CreateListDestroyViewSet, ListRetrieveViewSet
from api.serializers import (FavoriteRecipeSerializer, IngredientSerializer,
                             Recipe, RecipeSerializer, ShoppingСartSerializer,
                             TagSerializer)
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingСart,
                            Tag, User)
from rest_framework import generics, status, viewsets
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """Получение списка пользователей
    Добавление пользователя
    Получение данных отдельного пользователя
    Редактирование данных отдельного пользователя
    Удаление пользователя
    Получение данных личного профиля
    Редактирование личного профиля"""
    pass

class SubscribeViewSet(viewsets.ModelViewSet):
    pass

class TagViewSet(ListRetrieveViewSet):

    """Вьюсет для тегов. Доступны:
    Получение списка тегов.
    Полчение тега по id.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListRetrieveViewSet):

    """Вьюсет для ингредиентов. Доступны:
    Получение списка ингридиентов.
    Полчение ингридиента по id.
    Подключена возможность поиска по имени.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter


class FavoriteRecipeViewSet(CreateListDestroyViewSet):

    """Вьюсет для избранных рецептов:
    Добавления рецепт в избранное.
    Удалить рецепт из избранного.
    """
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteRecipeSerializer

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.check_object_permissions(self.request, recipe)
        return recipe

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        self.request.favorite_recipe.recipe.add(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def preform_destroy(self, instance):
        self.request.user.favorite_recipe.recipe.remove(instance)


class ShoppingCartViewSet(ListRetrieveViewSet):

    """Вьюсет для списка покупок:
    Скачать список покупок.
    Добавления рецепт в список покупок.
    Удалить рецепт из списка покупок.
    """
    queryset = ShoppingСart.objects.all()
    serializer_class = ShoppingСartSerializer

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.check_object_permissions(self.request, recipe)
        return recipe

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        self.request.shopping_cart.recipe.add(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def preform_delete(self, instance):
        return self.request.user.shopping_cart.recipe.remove(instance)


class RecipeViewSet(viewsets.ModelViewSet):

    """Вьюсет для рецептов. Доступны:
    Получение списка рецептов;
    Созданние рецепта;
    Получение рецепта;
    Обновление рецепта;
    Удаление рецепта.
    """
    queryset = Recipe.objects.all()
    seializer_class = RecipeSerializer
    # def get_queryset(self):
    #     return Recipe.objects.annotate(
    #         is_favorited=Exists(
    #             FavoriteRecipe.objects.filter(
    #                 user=self.request.user, recipe=OuterRef('id'))),
    #         is_in_shopping_cart=Exists(
    #             ShoppingСart.objects.filter(
    #                 user=self.request.user, recipe=OuterRef('id')
    #             )
    #         )
    #     )
