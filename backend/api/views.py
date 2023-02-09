from io import BytesIO

from core.filters import IngredientFilter
from core.mixins import (CreateListDestroyRetrieveViewSet,
                        CreateListDestroyViewSet, ListRetrieveViewSet)
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, ShoppingСartSerializer,
                             SubscribeRecipeSerializer, SubscribeSerializer,
                             TagSerializer, TokenSerializer,
                             UserCreateSerializer, UserListSerializer,
                             UserPasswordSerializer)
from core.permissions import IsAdminOrReadOnly
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Exists, OuterRef, Value
from django.db.models.aggregates import Count, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Subscribe, Tag)
from users.models import User
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response


User = get_user_model()


DOCUMENT = 'shoppingcart.pdf'
SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

class UsersViewSet(UserViewSet):
    """Получение списка пользователей
    Добавление пользователя
    Получение данных отдельного пользователя
    Редактирование данных отдельного пользователя
    Удаление пользователя
    Получение данных личного профиля
    Редактирование личного профиля"""

    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.annotate(
            is_subscribed=Exists(
                self.request.user.follower.filter(author=OuterRef('id')))).prefetch_related(
            'follower', 'following'
        ) if self.request.user.is_authenticated else User.objects.annotate(
            is_subscribed=Value(False))

    def get_serializer_class(self):
        if self.request.method == 'post':
            return UserCreateSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,))

    def subscriptions(self, request):
        """Получить на кого пользователь подписан."""

        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        serializer = SubscribeSerializer(
            queryset, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


class AuthToken(ObtainAuthToken):
    """Авторизация пользователя."""

    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': token.key},
            status=status.HTTP_201_CREATED)


@api_view(['post'])
def set_password(request):
    """Функция для изменение пароля."""

    serializer = UserPasswordSerializer(
        data=request.data,
        context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Пароль успешно изменен!'},
            status=status.HTTP_201_CREATED)
    return Response(
        {'error': 'Проверьте вводимые данные!'},
        status=status.HTTP_400_BAD_REQUEST)


class SubscribeViewSet(CreateListDestroyRetrieveViewSet):
    """Подписывается на пользователей
    Отписывается от пользователей.
    """

    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.follower.select_related(
            'following'
        ).prefetch_related(
            'following__recipe'
        ).annotate(
            recipes_count=Count('following__recipe'),
            is_subscribed=Value(True), )

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(self.request, user)
        return user

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.id == instance.id:
            return Response(
                {'errors': 'Нельзя на самого себя подписываться!'},
                status=status.HTTP_400_BAD_REQUEST)
        if request.user.follower.filter(author=instance).exists():
            return Response(
                {'errors': 'Вы уже подписаны!'},
                status=status.HTTP_400_BAD_REQUEST)
        subs = request.user.follower.create(author=instance)
        serializer = self.get_serializer(subs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.follower.filter(author=instance).delete()


class TagViewSet(ListRetrieveViewSet):
    """Вьюсет для тегов. Доступны:
    Получение списка тегов.
    Полчение тега по id.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ListRetrieveViewSet):
    """Вьюсет для ингредиентов. Доступны:
    Получение списка ингридиентов.
    Полчение ингридиента по id.
    Подключена возможность поиска по имени.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)


class FavoriteRecipeViewSet(CreateListDestroyViewSet):
    """Вьюсет для избранных рецептов:
    Добавления рецепт в избранное.
    Удалить рецепт из избранного.
    """

    queryset = FavoriteRecipe.objects.all()
    serializer_class = SubscribeRecipeSerializer

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

    queryset = ShoppingCart.objects.all()
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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        return Recipe.objects.annotate(
            is_favorited=Exists(
                FavoriteRecipe.objects.filter(
                    user=self.request.user, recipe=OuterRef('id'))),
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    user=self.request.user,
                    recipe=OuterRef('id')))
        ).select_related('author').prefetch_related(
            'tags', 'ingredients', 'recipe',
            'shopping_cart', 'favorite_recipe'
        ) if self.request.user.is_authenticated else Recipe.objects.annotate(
            is_in_shopping_cart=Value(False),
            is_favorited=Value(False),
        ).select_related('author').prefetch_related(
            'tags', 'ingredients', 'recipe',
            'shopping_cart', 'favorite_recipe')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Функция для загрузки списка ингредиентов."""

        buffer = BytesIO()
        page = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        x_position, y_position = 50, 800
        shopping_cart = (
            request.user.shopping_cart.recipe.
            values(
                'ingredients__name',
                'ingredients__measurement_unit'
            ).annotate(amount=Sum('recipe__amount')).order_by())
        page.setFont('Vera', 14)
        if shopping_cart:
            indent = 20
            page.drawString(x_position, y_position, 'Cписок покупок:')
            for index, recipe in enumerate(shopping_cart, start=1):
                page.drawString(
                    x_position, y_position - indent,
                    f'{index}. {recipe["ingredients__name"]} - '
                    f'{recipe["amount"]} '
                    f'{recipe["ingredients__measurement_unit"]}.')
                y_position -= 15
                if y_position <= 50:
                    page.showPage()
                    y_position = 800
            page.save()
            buffer.seek(0)
            return FileResponse(
                buffer, as_attachment=True, DOCUMENT=DOCUMENT)
        page.setFont('Vera', 24)
        page.drawString(
            x_position,
            y_position,
            'Cписок покупок пуст!')
        page.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, DOCUMENT=DOCUMENT)
