from django.contrib import admin

from .models import Category, Genre, Title, User, Review, Comment


class UserAdmin(admin.ModelAdmin):
    """Настройка админки пользователей."""
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'bio', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    """Настройка админки категорий произведений."""
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    """Настройка админки жанров произведений."""
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    """Настройка админки произведений."""
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'description')
    list_filter = ('genre', 'year')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Настройка админки отзывов к произведеням."""
    list_display = ('id', 'author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('score', 'author', 'pub_date')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Настройка админки комментариев к отзывам."""
    list_display = ('id', 'author', 'review', 'text', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
