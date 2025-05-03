# -*- coding: utf-8 -*-
"""
paging structs module.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CorePagination(PageNumberPagination):
    """
    core pagination class.
    """

    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(
            {
                'num_pages': self.page.paginator.num_pages,
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data,
            }
        )


class LargePagination(CorePagination):
    """
    large pagination class.
    """

    page_size = 48


class MediumPagination(CorePagination):
    """
    medium pagination class.
    """

    page_size = 10


class SmallPagination(CorePagination):
    """
    small pagination class.
    """

    page_size = 5
