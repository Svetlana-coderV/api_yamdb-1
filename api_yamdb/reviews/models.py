from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель кастомных пользователей."""
    username = models.TextField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLES,
        default=USER
    )

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


# class Category(models.Model):
#     """Модель категорий произведений."""
#     pass


# class Genre(models.Model):
#     """Модель жанров произведений."""
#     pass


# class Title(models.Model):
#     """Модель произведения."""
#     pass


# class Review(models.Model):
#     """Модель отзывов."""
#     pass


# class Comment(models.Model):
#     """Модель комментариев к отзывам."""
#     pass
