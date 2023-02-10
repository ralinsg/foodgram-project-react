from django.core.exceptions import ValidationError


def validate_min(value):
    """Валидация поля amount.
    Функция проверяет минимальное количество ингредиентов."""

    if value < 1:
        raise ValidationError(
            f'Минимальное значение не может быть меньше 1'
        )
