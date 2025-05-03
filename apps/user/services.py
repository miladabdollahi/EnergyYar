from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.user.models import User


def get_user(raise_exception=False, **filters):
    """
    Retrieve a single user instance based on the provided filters

    :param bool raise_exception: raise exception.
    :param filters: Filters to locate the user (e.g., username, email, etc.).
    :type filters: dict

    :raises ValidationError: user not found error.

    :rtype: User
    """

    try:
        return User.objects.get(**filters)
    except User.DoesNotExist:
        if raise_exception:
            raise ValidationError(
                _('User with this [{filters}] filters not found.').format(filters=filters)
            )
    except User.MultipleObjectsReturned:
        if raise_exception:
            raise ValidationError(
                _(
                    'User with this [{filters}] filters don`t be unique.'
                ).format(filters=filters)
            )


def update_user(user, **kwargs):
    """
    update user.

    :param User user: user instance.
    """

    update_fields = ['modified_time']
    for key, value in kwargs.items():
        if kwargs.get("password"):
            user.set_password(value)
        else:
            setattr(user, key, value)
        update_fields.append(key)

    user.save(update_fields=update_fields)


def create_user(**kwargs):
    """
    Create a user.

    :param kwargs: Information such as username, mobile, email,  firstname, lastname, etc.

    :return: User instance.

    :raises ValidationError: If username, email, mobile is duplicate.
    """

    return User.objects.create_user(**kwargs)


def delete_user(user):
    """
    Delete a user.

    :param User user: user instance.
    """

    user.delete()
