from django.urls import path, include
from rest_framework import routers

from .views import send_confirmation_code, get_jwt_token, UsersViewSet
from .views import ReviewViewSet, CommentViewSet


app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register('titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'

)

urlpatterns = [
    path(
        'auth/signup/', send_confirmation_code),
    path('auth/token/', get_jwt_token),
    path('', include(router_v1.urls)),
]
