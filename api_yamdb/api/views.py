from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from reviews.models import Category, Genre, Title, User
from .filter import TitleFilter
from .mixins import DestroyCreateListMixins
from .serializers import (
    CategoriesSerializer, GenresSerializer, SendCodeSerializer,
    GetJWTSerializer, UserSerializer, TitlesGetSerializer, TitlesPostSerializer
)
from .permissions import IsAdminOrSuperUser


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if any((
            User.objects.filter(username=username).exists(),
            User.objects.filter(email=email).exists()
    )):
        return Response(
            {"Такой username или e-mail уже используется."},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        User.objects.create_user(username=username, email=email)
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код подтверждения: {confirmation_code}'
    mail_subject = 'Код подтверждения на YaMDb'
    send_mail(mail_subject, message, settings.TOKEN_EMAIL, [email])
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def get_jwt_token(request):
    serializer = GetJWTSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        old_response_data = super(UsersViewSet, self).list(request, *args,
                                                           **kwargs)
        new_response_data = [old_response_data.data]
        return Response(new_response_data)


class CategoryViewSet(DestroyCreateListMixins):
    """Вьюсет для модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenreViewSet(DestroyCreateListMixins):
    """Вьюсет для модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleFilter
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesPostSerializer
