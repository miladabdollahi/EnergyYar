# -*- coding: utf-8 -*-
"""
core viewsets module.
"""

from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.core.utils import make_iterable


class CoreViewSet(viewsets.GenericViewSet):
    """
    core view set class.

    every view set must be subclassed from this.
    """

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = '__all__'

    # every subclass must set a default queryset here.
    queryset = None

    # every subclass must set a default serializer class here.
    serializer_class = None

    # every subclass must set a default permission class here.
    permission_classes = None

    pagination_class = None

    # a dict containing different method names and related queryset for each service.
    # in the form of: {'method_name': Queryset}
    querysets = {}

    # a dict containing different method names and related serializer classes.
    # in the form of: {'method_name': SerializerClass}
    # {'list': ListSerializer, 'register': RegisterSerializer}
    serializers = {}

    # a dict containing different method names and related permission classes.
    # in the form of: {'method_name': PermissionClass}
    # {'list': IsDealerAuthenticated, 'register': IsEmployeeAuthenticated}
    permissions = {}

    pagination_classes = {}

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            pagination_class = self.pagination_classes.get(self.action, self.pagination_class)
            self._paginator = None

            if callable(pagination_class):
                self._paginator = pagination_class()

            if isinstance(pagination_class, dict):
                pagination_class = pagination_class.get(
                    self.request.method.lower(), self.pagination_class)

                if callable(pagination_class):
                    self._paginator = pagination_class()

        return self._paginator

    def get_queryset(self, **kwargs):
        """
        gets the related queryset to the current method.

        it returns the default `queryset` if the method has no custom queryset.
        """

        assert (self.queryset is not None or len(self.querysets) != 0), (
                "'%s' should either include `queryset` or 'querysets' attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.querysets.get(self.action, self.queryset)

        if isinstance(queryset, QuerySet):
            return queryset.filter(**kwargs).all()

        if callable(queryset):
            queryset = queryset()
            if isinstance(queryset, QuerySet):
                return queryset.filter(**kwargs).all()

        if isinstance(queryset, dict):
            queryset = queryset.get(self.request.method.lower(), self.queryset)
            if callable(queryset):
                queryset = queryset()
                if isinstance(queryset, QuerySet):
                    return queryset.filter(**kwargs).all()

        return queryset

    def get_serializer_class(self):
        """
        gets the related serializer to the current method.

        it returns the default `serializer_class` if the method has no custom serializer.
        """

        serializer = self.serializers.get(self.action, self.serializer_class)
        if isinstance(serializer, dict):
            return serializer.get(self.request.method.lower(), self.serializer_class)

        return serializer

    def get_permissions(self):
        """
        gets the related permissions to the current method.

        it uses the default `permission_classes` if the method has no custom permission.
        """

        result = self.permissions.get(self.action, self.permission_classes)
        result = make_iterable(result)
        return [permission() for permission in result]

    def get_entity(self, id, *columns, **options):
        """
        gets an entity with given id and columns.

        :param int id: entity id.
        :param str columns: columns to be fetched.

        :return: model instance.
        """

        queryset = self.model.objects
        if columns is not None and len(columns) > 0:
            queryset = queryset.only(*columns)

        return get_object_or_404(queryset, pk=id)

    def options(self, request, *args, **kwargs):
        """
        Handler method for HTTP 'OPTIONS' request.
        """

        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().get_serializer_info(self.get_serializer())
        return Response(data, status=status.HTTP_200_OK)
