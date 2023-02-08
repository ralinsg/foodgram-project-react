import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Subscribe, Tag)
from rest_framework import serializers
User = get_user_model()
ERROR_MESSAGE = 'Не удается войти в систему с текущими данными'


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор данные для пользователей."""

    is_subscribed = serializers.BooleanField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed')


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализует данные для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'password',)

    def validate_password(self, password):
        validators.validate_password(password)
        return password


class UserPasswordSerializer(serializers.Serializer):
    """Сериализует данные для изменения пароля."""

    new_password = serializers.CharField(
        label='Новый пароль',
        help_text='Введите новый пароль'
    )
    current_password = serializers.CharField(
        label='Текущий пароль',
        help_text='Повторите текущий пароль'
    )

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if not authenticate(
                username=user.email,
                password=current_password):
            raise serializers.ValidationError(
                ERROR_MESSAGE, code='authorization')
        return current_password

    def create(self, data):
        user = self.context['request'].user
        password = make_password(
            data.get('new_password')
        )
        user.password = password
        user.save()
        return data

    def validate_new_password(self, new_password):
        validators.validate_password(new_password)
        return new_password


class TokenSerializer(serializers.Serializer):
    """Сериализует данные для получения токена."""

    email = serializers.CharField(
        label='Email',
        write_only=True
    )
    password = serializers.CharField(
        label='Пароль',
        write_only=True
    )
    token = serializers.CharField(
        label='Токен',
        read_only=True
    )


class SubscribeRecipeSerializer(serializers.ModelSerializer):
    """Сериализует данные для добавления рецепта в избранное."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',
        )


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализует данные для подписок и подписчиков"""

    email = serializers.EmailField(
        source='author.email',
        max_length=254
    )
    id = serializers.IntegerField(
        source='author.id'
    )
    username = serializers.CharField(
        source='author.username',
        max_length=150
    )
    first_name = serializers.CharField(
        source='author.first_name',
        max_length=150
    )
    last_name = serializers.CharField(
        source='author.last_name',
        max_length=150
    )
    is_subscribed = serializers.BooleanField(
        read_only=True
    )
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        read_only=True
    )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = (
            obj.author.recipe.all()[:int(limit)] if limit
            else obj.author.recipe.all())
        return SubscribeRecipeSerializer(
            recipes,
            many=True).data

    class Meta:
        model = Subscribe
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализует данные для получение списка тегов и тега по id"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализует данные для получение списка ингредиентов и ингредиента по id"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsEditSerializer(serializers.ModelSerializer):
    """Серилизатор для ингредиентов."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeUserSerializer(serializers.ModelSerializer):
    """Сериализует данные рецепта."""

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()

    is_subscribed = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed')


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализует данные для списка избранного."""

    class Meta:
        model = FavoriteRecipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ShoppingСartSerializer(serializers.Serializer):
    """Сериализует данные для корзины покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для описания ингредиентов в рецепте."""

    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'measurement_unit', 'amount')


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта.
    Валидирует данные и возвращает RecipeReadSerializer."""

    author = UserListSerializer(read_only=True)

    image = Base64ImageField(
        max_length=None,
        use_url=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    ingredients = IngredientsEditSerializer(
        many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time'
        )

    def validate(self, data):
        list = [item['ingredient'] for item in data['ingredients']]
        all_ingr, distinct_ingr = (
            len(list), len(set(list)))

        if all_ingr != distinct_ingr:
            raise serializers.ValidationError(
                {'error': 'Ингредиенты должны быть уникальными'}
            )
        return data

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                'Время приготовления >= 1!')
        return cooking_time

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Мин. 1 ингредиент в рецепте!')
        for ingredient in ingredients:
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Количество ингредиента >= 1!')
        return ingredients

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'), )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeReadSerializer(instance, context=context).data

class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения информации о рецепте."""

    image = Base64ImageField()
    tags = TagSerializer(
        many=True,
        read_only=True)
    author = RecipeUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True,
        source='recipe')
    is_favorited = serializers.BooleanField(
        read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
