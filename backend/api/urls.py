from api.views import (AuthToken, FavoriteRecipeViewSet, IngredientViewSet,
                       RecipeViewSet, ShoppingCartViewSet, SubscribeViewSet,
                       TagViewSet, UsersViewSet, set_password)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UsersViewSet)
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
    name='favorite_recipe'
    ),
    path(
    'recipes/<int:recipe_id>/shopping_cart/',
    ShoppingCartViewSet,
    name='shopping_cart'
    ),
    path(
    'auth/token/login/',
    AuthToken,
    name='login'
    ),
    path(
    'users/set_password/',
    set_password,
    name='set_password'
    ),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
