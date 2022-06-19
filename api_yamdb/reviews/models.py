from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


class User(AbstractUser):
    """Кастомная модель пользователей."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.TextField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=25,
        choices=ROLES,
        default=USER
    )

    @property
    def is_admin(self):
        """Проверка, является ли пользователь админом или суперюзером."""
        return (
            self.role == self.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        """Проверка, является ли пользователь модератором."""
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение'
    )
    year = models.PositiveSmallIntegerField(
        validators=(validate_year,),
        verbose_name='Дата выхода'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов к произведениям."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name='Текст отзыва')
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name='Рейтинг произведения'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
