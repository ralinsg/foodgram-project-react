from core.models import CreatedModel
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Tag(CreatedModel):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Максимум 200 символов',
        db_index=True,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        help_text='Цвет в HEX'
    )
    slug = models.SlugField(
        verbose_name='Cсылка',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(CreatedModel):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Максимум 200 символов',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения',
        help_text='Максимум 200 символов'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Список ингредиентов',
        through='RecipeIngredient'
    )
    is_favorited = models.BooleanField(
        blank=True,
        verbose_name='Находится ли в избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        blank=True,
        verbose_name='Находится ли в корзине'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Максимум 200 символов'
    )
    image = models.ImageField(
        verbose_name='Ссылка на картинку на сайте',
        upload_to='static/recipe/',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Не может быть меньше 1 минуты'
    )
    slug = models.SlugField(
        verbose_name='Cсылка',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Subscribe(CreatedModel):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'author']


class ShoppingСart(CreatedModel):
    user = models.OneToOneField(
        User,
        related_name='shopping_cart',
        verbose_name='Пользователь',
        null=True,
        on_delete=models.CASCADE
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Покупка'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return self.recipe


class FavoriteRecipe(CreatedModel):
    user = models.OneToOneField(
        User,
        related_name='favorite_recipe',
        verbose_name='Пользователь',
        null=True,
        on_delete=models.CASCADE
    )
    recipe = models.ManyToManyField(
        Recipe,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в избранные.'


class RecipeIngredient(CreatedModel):
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ingredient',
        on_delete=models.CASCADE
    )

    amount = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
        validators=(
        validators.MinValueValidator(
        1, message='Минимальное количество не может быть меньше 1'),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return self.name
