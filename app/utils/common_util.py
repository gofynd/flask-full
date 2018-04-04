import time
import re
from datetime import datetime

from flask import url_for as _url_for, current_app, _request_ctx_stack

from app.constants import ISO_DATE_FORMAT


def timestamp():
    """Return the current timestamp as an integer."""
    return int(time.time())


def url_for(*args, **kwargs):
    """
    url_for replacement that works even when there is no request context.
    """
    if '_external' not in kwargs:
        kwargs['_external'] = False
    reqctx = _request_ctx_stack.top
    if reqctx is None:
        if kwargs['_external']:
            raise RuntimeError('Cannot generate external URLs without a '
                               'request context.')
        with current_app.test_request_context():
            return _url_for(*args, **kwargs)
    return _url_for(*args, **kwargs)


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        if word:
            result.append(word)
    return delim.join(result)


class DateHelper(object):

    @staticmethod
    def convert_date_to_string(date, date_format=ISO_DATE_FORMAT):
        """
        :param date: Object of class datetime.datetime
        :return: string
        """
        return datetime.strftime(date, date_format)

