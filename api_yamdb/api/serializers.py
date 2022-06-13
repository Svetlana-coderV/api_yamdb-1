from rest_framework import serializers

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
