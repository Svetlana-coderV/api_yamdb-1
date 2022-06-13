from django.urls import path, include
from rest_framework import routers

from .views import send_confirmation_code, get_jwt_token, UsersViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path(
        'auth/signup/', send_confirmation_code),
    path('auth/token/', get_jwt_token),
    path('', include(router_v1.urls)),
]
