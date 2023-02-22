from api.views import (AuthToken, FavoriteRecipeViewSet, IngredientViewSet,
                       RecipeViewSet, ShoppingCartViewSet, SubscribeViewSet,
                       TagViewSet, UsersViewSet, set_password)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)


urlpatterns = [
    path(
    'auth/token/login/',
    AuthToken.as_view(),
    name='login'
    ),
    path(
    'users/set_password/',
    set_password,
    name='set_password'
    ),
    path(
    'users/<int:user_id>/subscribe/',
    SubscribeViewSet.as_view(),
    name='subscribe'
    ),
    path(
    'recipe/<int:recipe_id>/favorite/',
    FavoriteRecipeViewSet.as_view(),
    name='favorite_recipe'
    ),
    path(
    'recipes/<int:recipe_id>/shopping_cart/',
    ShoppingCartViewSet.as_view(),
    name='shopping_cart'
    ),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
