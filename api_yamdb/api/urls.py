from django.urls import path, include
from rest_framework import routers

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet,
    send_confirmation_code, get_jwt_token, UsersViewSet,
)


app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path(
        'auth/signup/', send_confirmation_code),
    path('auth/token/', get_jwt_token),
    path('', include(router_v1.urls)),
]
