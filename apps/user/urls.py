from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from apps.user.api import UserViewSet

app_name = 'user'

urlpatterns = [
    path('user/login/', ObtainAuthToken.as_view(), name='login'),
]

v1_router = routers.DefaultRouter()
v1_router.register('user', UserViewSet, 'UserViewSet')

urlpatterns += v1_router.urls
