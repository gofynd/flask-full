import json
import requests
from functools import wraps

import datetime
from flask import current_app
from flask import g
from flask import jsonify
from flask import request
import logging

logger = logging.getLogger(__name__)


def check_authentication():
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            logger.debug("in auth decorator")
            if current_app.config['IS_AUTH_ENABLED']:
                # code to check auth should be here
                logger.debug("AUTH is ENABLED")
                user_info = {"username": "", "user_id": ""}
                g.user_info = user_info
                logger.info("REMOTE_ADDR: {} METHOD: {} URL: {} USERNAME: {} USER_ID: {} \nDATA: {}".format(request.remote_addr, request.method,
                                                                                 request.url, user_info['username'], user_info['user_id'], request.data))
            else:
                logger.debug("AUTH is DISABLED")
                logger.info("REMOTE_ADDR: {} METHOD: {} URL: {} \nDATA: {}".format(request.remote_addr, request.method,
                                                                                 request.url, request.data))

            return f()
        return decorated_function

    return login_required




# # Authentication objects for username/password auth, token auth, and a
# # token optional auth that is used for open endpoints.
# basic_auth = HTTPBasicAuth()
# token_auth = HTTPTokenAuth('Bearer')
# token_optional_auth = HTTPTokenAuth('Bearer')
#
#
# @basic_auth.verify_password
# def verify_password(nickname, password):
#     """Password verification callback."""
#     if not nickname or not password:
#         return False
#     return True
#
#
# @basic_auth.error_handler
# def password_error():
#     """Return a 401 error to the client."""
#     # To avoid login prompts in the browser, use the "Bearer" realm.
#     return (jsonify({'error': 'authentication required'}), 401,
#             {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})
#
#
# @token_auth.verify_token
# def verify_token(token, add_to_session=False):
#     """Token verification callback."""
#     if add_to_session:
#         # clear the session in case auth fails
#         if 'nickname' in session:
#             del session['nickname']
#     return True
#
#
# @token_auth.error_handler
# def token_error():
#     """Return a 401 error to the client."""
#     return (jsonify({'error': 'authentication required'}), 401,
#             {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})
#
#
# @token_optional_auth.verify_token
# def verify_optional_token(token):
#     """Alternative token authentication that allows anonymous logins."""
#     if token == '':
#         # no token provided, mark the logged in users as None and continue
#         g.current_user = None
#         return True
#     # but if a token was provided, make sure it is valid
#     return verify_token(token)
