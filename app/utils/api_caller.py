import logging
from datetime import datetime

from requests import api
from app import signals
from app.exceptions import APICallError

logger = logging.getLogger(__name__)


class APICaller(object):

    def call_api(self, method, url, raise_exception_on_error=False, **kwargs):
        logger.debug("in call_api method of APICaller")
        logger.debug("request method is {} url is {} args are {}".format(method, url, kwargs))
        logger.debug("emitting pre_call_api signal")

        signals.pre_call_api.send(method=method, **kwargs)

        response = api.request(method, url, **kwargs)

        logger.debug("response of api request is {}".format(response))
        logger.debug("emitting post_call_api signal with args {}".format(kwargs))
        datetime_str = datetime.now()
        signal_arguments = {
            "method": method,
            "url": url,
            "datetime_str": datetime_str,
            "status_code": response.status_code,
            "response": response.text,
            "other": None
        }
        # data/json is included in kwargs
        signals.post_call_api.send(**signal_arguments, **kwargs)

        if raise_exception_on_error and response.status_code != 200:
            raise APICallError(response.status_code, response.text)

        return response