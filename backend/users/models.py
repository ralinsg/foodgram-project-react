from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'
    CHOICES = [
        (GUEST, 'Guest'),
        (USER, 'User'),
        (ADMIN, 'Administrator'),
    ]
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        help_text='Максимум 254 символа',
        unique=True
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Уникальный юзернейм',
        help_text='Максимум 150 символов',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Максимум 150 символов'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Максимум 150 символов'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Максимум 150 символов'
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=CHOICES,
        default=USER
    )
    @property
    def is_guest(self):
        return self.role == self.GUEST

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username
