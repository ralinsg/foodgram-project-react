from django.core.exceptions import ValidationError

value = 2
def validate_min(value):
    """Валидация поля amount.
    Функция проверяет минимальное количество ингредиентов."""

    if value.count() < 1:
        raise ValidationError(
            f'Минимальное значение не может быть меньше 1'
        )
