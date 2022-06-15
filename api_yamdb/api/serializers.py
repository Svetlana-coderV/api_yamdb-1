from rest_framework import serializers
from reviews.models import Review, Comment

from reviews.models import User


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'author', 'title', 'text', 'score', 'pub_date'
        )
        read_only_fields = ('title', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title', 'author', 'review', 'text', 'pub_date'
        )
        read_only_fields = ('title', 'review', 'pub_date')
        model = Comment
