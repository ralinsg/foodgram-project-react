from django.contrib import admin
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Subscribe, Tag)

EMPTY = 'пусто'


class RecipeIngredientAdmin(admin.StackedInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    inlines = (RecipeIngredientAdmin,)
    empty_value_display = EMPTY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    search_fields = ('name', 'slug',)
    empty_value_display = EMPTY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name', 'measurement_unit',)
    empty_value_display = EMPTY


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    list_filter = (
        'user',
    )
    search_fields = (
        'user__email', 'author__email',)
    empty_value_display = EMPTY


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user'
    )
    list_filter = (
        'user',
    )
    empty_value_display = EMPTY


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user'
    )
    list_filter = (
        'user',
    )
    empty_value_display = EMPTY
