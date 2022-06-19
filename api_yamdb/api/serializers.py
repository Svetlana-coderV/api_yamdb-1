from rest_framework import serializers

from reviews.models import Category, Genre, Title, User, Review, Comment


class SendCodeSerializer(serializers.Serializer):
    """Сериализатор для отправки кода подтверждения."""
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True)

    def validate_username(self, value):
        """Запрет использования username 'me'."""
        if value == 'me':
            raise serializers.ValidationError(
                "Такое имя использовать запрещено")
        return value


class GetJWTSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitlesPostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запросов к произведениям."""
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitlesGetSerializer(serializers.ModelSerializer):
    """Сериализатор для GET-запросов к произведениям."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов к произведениям."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        exclude = ('title',)
        read_only_fields = ('pub_date',)
        model = Review

    def validate(self, data):
        """Запрет публицакии только одного отзыва на каждое произведение."""
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        review = Review.objects.filter(
            author=author, title=title_id
        )
        if review.exists():
            raise serializers.ValidationError(
                'На каждое произведение можно опубликовать только один отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к отзывам."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        exclude = ('review',)
        read_only_fields = ('review', 'pub_date')
        model = Comment
