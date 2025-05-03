from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import apps.user.services as user_services
from apps.core.viewsets import CoreViewSet
from apps.user.models import User
from apps.user.serializers import (
    UserListSerializer, UserRetrieveSerializer, UserCreateSerializer, UserUpdateSerializer, UserBaseSerializer
)


class UserViewSet(viewsets.ModelViewSet, CoreViewSet):
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer

    lookup_field = "slug"

    serializers = {
        "list": UserListSerializer,
        "retrieve": UserRetrieveSerializer,
        "create": UserCreateSerializer,
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer,
    }

    permissions = {
        "logout": IsAuthenticated,
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_services.create_user(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = user_services.get_user(raise_exception=True, **kwargs)

        if user not in (None, ""):
            serializer = self.get_serializer(data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            user_services.update_user(user, **serializer.validated_data)

            return Response(status=status.HTTP_200_OK)

        raise NotFound()

    @action(methods=['DELETE'], detail=False, url_path='logout')
    def logout(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
