from xml.etree.ElementTree import Comment
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

from reviews.models import Category, Genre, Title, User, Review, Comment
from .filter import TitleFilter
from .mixins import DestroyCreateListMixins
from .serializers import (
    CategoriesSerializer, GenresSerializer, SendCodeSerializer,
    GetJWTSerializer, UserSerializer, TitlesGetSerializer, TitlesPostSerializer,
    ReviewSerializer, CommentSerializer
)
from .permissions import (
    IsAdminOrSuperUser, IsAdminOrReadOnly, IsAuthorOrIsStaff
)


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
            {'token': str(refresh.access_token)},
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
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        old_response_data = super(CategoryViewSet, self).list(request, *args,
                                                              **kwargs)
        new_response_data = [old_response_data.data]
        return Response(new_response_data)


class GenreViewSet(DestroyCreateListMixins):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        old_response_data = super(GenreViewSet, self).list(request, *args,
                                                           **kwargs)
        new_response_data = [old_response_data.data]
        return Response(new_response_data)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitlesGetSerializer
        return TitlesPostSerializer

    def list(self, request, *args, **kwargs):
        old_response_data = super(TitleViewSet, self).list(request, *args,
                                                           **kwargs)
        new_response_data = [old_response_data.data]
        return Response(new_response_data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrIsStaff]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def list(self, request, *args, **kwargs):
        old_response_data = super(ReviewViewSet, self).list(request, *args,
                                                            **kwargs)
        new_response_data = [old_response_data.data]
        return Response(new_response_data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrIsStaff]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title, review=review)

    def list(self, request, *args, **kwargs):
        old_response_data = super(CommentViewSet, self).list(request, *args,
                                                             **kwargs)
        new_response_data = [old_response_data.data]
        return Response(new_response_data)
