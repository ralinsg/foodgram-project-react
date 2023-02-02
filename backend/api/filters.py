import django_filters as filters
from recipes.models import Ingredient


class IngredientFilter(filters.FilterSet):
    """Добавляет возможность поиска.
    Поиск частичному вхождению в начале названия ингредиента.
    """
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
