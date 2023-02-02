from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingСart,
                             Tag)
from rest_framework import serializers


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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализует данные."""
    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )


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
        model = ShoppingСart
        fields = '__all__'
