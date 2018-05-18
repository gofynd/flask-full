import logging
import os
import traceback
from datetime import datetime
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

from flask import Blueprint
from flask import jsonify
from flask import request
from flask.views import MethodView
from flask_mail import Message
from app.decorators.auth import check_authentication
from . import stats, config_name
from app import current_config
from app import mail

logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)


@main.before_app_request
@check_authentication()
def before_request():
    """Update requests per second stats."""
    # auditlog=AuditLog()
    # auditlog.api=request.url_rule.rule
    # auditlog.save()
    # import pdb;pdb.set_trace()

    # logger.info('Request data is : {}'.format(request.get_json()))
    stats.add_request()


@main.app_errorhandler(Exception)
def app_errorhandler(e):
    logger.debug('exception occured. Logging to collection...')
    logger.exception(e)

    # obj = APICallerLog(method=request.method.lower(), url=request.url, datetime=str(datetime.now()), status_code=500, response=traceback.format_exc(),
    #                          data=request.data, other=None, is_active=True).save()
    # #
    # # logger.debug("datetime: {}".format(obj.datetime))
    # datetime_str = str(obj.datetime)
    # parse_result = urlparse(request.url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parse_result)

    if current_config.IS_ERROR_MAIL_ENABLED:
        # send error mail
        mail_subject = "[App Name] {}".format(str(e))
        if config_name != 'production':
            mail_subject = "[App Name {}] {}".format(config_name, str(e))

        msg = Message(subject=mail_subject, body=traceback.format_exc(), sender=current_config.DEFAULT_MAIL_SENDER, recipients=current_config.ADMINS)
        mail.send(msg)

    # return jsonify({'message': "Internal server error!!!", "success": False, "datetime": datetime_str,
    #                 "error_details_api": "{}api-error-log/?datetime={}".format(domain, datetime_str.replace(" ", '%20'))}), 500


class PingPongView(MethodView):
    """PingPongView apis"""

    def get(self, *args, **kwargs):
        return jsonify({'message': 'pong'})


main.add_url_rule('/ping/', view_func=PingPongView.as_view('ping'))

# class APIErrorLogView(MethodView):
#     """APIErrorLog apis"""
#
#     @get_request.get(APICallerLog, GetErrorLogSerailzer, True, None)
#     def get(self, *args, **kwargs):
#         pass
#
#
# class CeleryErrorLogView(MethodView):
#     """CeleryErrorLog apis"""
#
#     @get_request.get(CeleryErrorLog, GetCeleryErrorLogSerailzer, True, None)
#     def get(self, *args, **kwargs):
#         pass
#
# main.add_url_rule('/api-error-log/', view_func=APIErrorLogView.as_view('api_error_log'))
# main.add_url_rule('/celery-error-log/', view_func=CeleryErrorLogView.as_view('celery_error_log'))


# @main.before_app_first_request
# def before_first_request():
#     """Start a background thread that looks for users that leave."""
#     def find_offline_users(app):
#         with app.app_context():
#             while True:
#                 # users = User.find_offline_users()
#                 # for user in users:
#                 #     push_model(user)
#                 db.session.remove()
#                 time.sleep(5)
#
#     if not current_app.config['TESTING']:
#         thread = threading.Thread(target=find_offline_users,
#                                   args=(current_app._get_current_object(),))
#         thread.start()
#
# @main.route('/')
# def index():
#     """Serve client-side application."""
#     return render_template('index.html')
#
# @main.route('/stats', methods=['GET'])
# def get_stats():
#     return jsonify({'requests_per_second': stats.requests_per_second()})

