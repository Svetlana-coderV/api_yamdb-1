from django.contrib import ModelAdmin, admin

from .models import Category, Genre, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'bio', 'role')
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CommentAdmin(ModelAdmin):
    list_display = ('id', 'author', 'title', 'review', 'pub_date', 'text')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')


class GenreAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug')


class TitleAdmin(ModelAdmin):
    list_display = ('id', 'name', 'year', 'description')
    search_fields = ('description',)
    list_filter = ('genre', 'year')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
