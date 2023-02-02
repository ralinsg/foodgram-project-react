from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                    FavoriteRecipeViewSet, TagViewSet, SubscribeViewSet)

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path(
        'users/<int:user_id>/subscribe/',
        SubscribeViewSet,
        name='subscribe'
    ),
    path(
    'recipe/<int:recipe_id>/favorite/',
    FavoriteRecipeViewSet,
    name='favorite'
    ),
    path(
    'recipes/<int:recipe_id>/shopping_cart/',
    ShoppingCartViewSet,
    name='shopping_cart'
    ),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
