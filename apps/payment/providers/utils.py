import uuid
from urllib import parse

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def append_querystring(url, params):
    url_parts = list(parse.urlparse(url))
    query = dict(parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = parse.urlencode(query)

    return parse.urlunparse(url_parts)


def generate_tracking_code():
    return int(str(uuid.uuid4().int)[-1 * 64:])


def base64_encode(text):
    """
    gets the base64 encoded version of given string value.

    :param str text: value to be encoded.

    :rtype: str
    """

    return urlsafe_base64_encode(force_bytes(text))
