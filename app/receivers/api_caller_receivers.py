import logging
from app.signals import post_call_api


logger = logging.getLogger(__name__)


@post_call_api.connect
def on_post_call_api_signal(sender, method, url, datetime_str, status_code, response, other, **kwargs):
    logger.debug("in post_call_api receiver. kwargs are {}".format(kwargs))

