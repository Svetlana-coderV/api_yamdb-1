from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Такое имя использовать запрещено")
        return value


class GetJWTSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = Genre
        lookup_field = 'slug'


class TitlesPostSerializer(serializers.ModelSerializer):
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
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title
