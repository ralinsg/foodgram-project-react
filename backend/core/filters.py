from django.core.exceptions import ValidationError
import django_filters as filters

from users.models import User
from recipes.models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """Добавляет возможность поиска по ингредиентам.
    Поиск частичному вхождению в начале названия ингредиента.
    """
    name = filters.CharFilter(lookup_expr='istartswith')


    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='В корзине.')
    is_favorited = filters.BooleanFilter(
        widget=filters.widgets.BooleanWidget(),
        label='В избранных.')
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Ссылка')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']
