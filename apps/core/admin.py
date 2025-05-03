from apps.core.utils import make_iterable
from django.contrib import admin
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html


class ModelAdminBase(admin.ModelAdmin):
    """
    base model admin class.

    all of 'ModelAdmin' classes must be extended from this one instead of 'admin.ModelAdmin'.
    """

    list_display = ()
    _list_display = ('id',)
    _search_fields = ('id',)
    _readonly_fields = ('created_time', 'modified_time')
    _list_exclude = (models.ManyToManyField,)

    def __init__(self, model, admin_site):
        if len(self.list_display) == 0:
            self.list_display = [
                field.name for field in model._meta.fields
                if type(field) not in self._list_exclude and
                field.name not in self._list_display
            ]

        super().__init__(model, admin_site)

    def get_search_fields(self, request):
        """
        gets all search fields of this admin class.

        :rtype: tuple
        """

        base_search_fields = make_iterable(self._search_fields, tuple)
        custom_search_fields = make_iterable(self.search_fields, tuple)
        return tuple(set(base_search_fields + custom_search_fields))

    def get_list_display(self, request):
        """
        gets the list display of this admin class.

        :rtype: tuple
        """

        base_list_display = make_iterable(self._list_display, tuple)
        custom_list_display = make_iterable(self.list_display, tuple)
        return base_list_display + custom_list_display

    def get_readonly_fields(self, request, obj=None):
        """
        gets the readonly fields of this admin class

        :rtype: tuple
        """

        base_readonly_fields = make_iterable(self._readonly_fields, tuple)
        custom_readonly_fields = make_iterable(self.readonly_fields, tuple)
        return tuple(set(base_readonly_fields + custom_readonly_fields))

    def get_list_page(self, model_class, title, **filters):
        """
        gets a link to list page of a related entity.

        :param Model model_class: related model class.
        :param str title: title of link button.
        :keyword **filters: filters to be passed to related list page.

        :rtype: str
        """

        content_type = ContentType.objects.get_for_model(model_class)
        content_type_url = reverse(
            f'admin:{content_type.app_label}_{content_type.model}_changelist'
        )
        combined_filters = '&'.join([f'{key}={value}' for key, value in filters.items()])
        content_type_url += f'?{combined_filters}'
        html = f'<button class="button btn" type="button" ' \
            f'onclick="window.open(\'{content_type_url}\')" >' \
            f' {title}</button>'

        return format_html(html)

    def get_detail_page(self, model_class, pk, items_title=None, title='Details', button=False):
        """
        gets a link to detail page of a related entity.

        it returns None if pk is None.

        :param Model model_class: related model class.
        :param int pk: primary key of related entity.
        :param items_title: represent title of items in admin panel tables

        :param str title: title of link button.
                          this will only be used if button=True is provided.

        :param bool button: render a button instead of a link.

        :rtype: str
        """

        if pk is None:
            return None

        content_type = ContentType.objects.get_for_model(model_class)
        content_type_change_url = reverse(
            f'admin:{content_type.app_label}_{content_type.model}_change',
            args=(pk,)
        )

        if button is True:
            html = f'<button class="button btn" type="button" ' \
                f'onclick="window.open(\'{content_type_change_url}\')" >' \
                f' {title}</button>'
        else:
            if items_title:
                html = f'<a href="{content_type_change_url}">{items_title}</a>'
            else:
                html = f'<a href="{content_type_change_url}">{pk}</a>'

        return format_html(html)

    def get_detail_list_page(self, model_class, pk, title='Details', button=False):
        """
        gets a link to detail page of a related entity.

        it returns None if pk is None.

        :param Model model_class: related model class.
        :param int pk: primary key of related entity.

        :rtype: str
        """

        if pk is None:
            return None

        content_type = ContentType.objects.get_for_model(model_class)
        content_type_change_url = reverse(
            f'admin:{content_type.app_label}_{content_type.model}_changelist'
        )
        content_type_change_url += f'?id={pk}'

        if button is True:
            html = f'<button class="button btn" type="button" ' \
                f'onclick="window.open(\'{content_type_change_url}\')" >' \
                f' {title}</button>'
        else:
            html = f'<a href="{content_type_change_url}">{pk}</a>'

        return format_html(html)