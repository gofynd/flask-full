import configparser

from flasgger import Swagger

meta = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

meta.read('meta.cfg')
app_name = meta['app']['name']


if meta['app']['enable_eventlet']=='true':
    import eventlet
    eventlet.monkey_patch()

import os
# get redis and mongo host
redis_host = os.environ.get("redis_host", '127.0.0.1')
mongo_host = os.environ.get("mongo_host", '127.0.0.1')

import logging
import sys
from collections import namedtuple
from logging.handlers import RotatingFileHandler
import boto3
import redis as redis
from boto3.s3.transfer import S3Transfer
from celery import Celery
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO
from mongoengine import connect
from slackclient import SlackClient
from config import config
from app.utils.json_util import CustomFlaskJSONEncoder

ResultTuple = namedtuple('ResultTuple', ['data', 'errors', 'common'])


# current config
config_name = os.environ.get("{}_env".format(app_name), 'development')
current_config = config[config_name]

# Flask extensions
socketio = SocketIO()
cache = Cache(config=current_config.CACHE_CONFIG)
mail = Mail()

celery_app = Celery(__name__,
                broker=current_config.CELERY_BROKER_URL,
                backend=current_config.CELERY_RESULT_BACKEND)
celery_app.autodiscover_tasks([__name__])

slack_client = SlackClient(current_config.SLACK_TOKEN)

redis_client = redis.StrictRedis.from_url(current_config.REDIS_DOMAIN, db=0)

auth_redis_client = redis.StrictRedis.from_url(current_config.AUTH_REDIS_URL)

# s3 connection
# boto_client = boto3.client('s3', aws_access_key_id=current_config.AWS_ACCESS_KEY,
#                            aws_secret_access_key=current_config.AWS_SECRET_ACCESS_KEY)
# s3_transfer = S3Transfer(boto_client)


# Import Socket.IO events so that they are registered with Flask-SocketIO
from . import events  # noqa

log_formatter = logging.Formatter((
    '-' * 80 + '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
))


def create_app(main=True):
    app = Flask(__name__)
    swagger = Swagger(app)

    CORS(app, supports_credentials=True)
    app.config.from_object(current_config)
    app.json_encoder = CustomFlaskJSONEncoder
    # load celery config parameters
    celery_app.config_from_object(current_config)

    # Initialize flask extensions
    cache.init_app(app)
    mail.init_app(app)

    # mongoengine connection
    connect(**app.config['MONGO_DATABASES']['app'])

    if main:
        # Initialize socketio server and attach it to the message queue, so
        # that everything works even when there are multiple servers or
        # additional processes such as Celery workers wanting to access
        # Socket.IO
        socketio.init_app(app,
                          message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])
    else:
        # Initialize socketio to emit events through through the message queue
        # Note that since Celery does not use eventlet, we have to be explicit
        # in setting the async mode to not use it.
        socketio.init_app(None,
                          message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'],
                          async_mode='threading')

    # Import models so that they are registered with app
    from . import models  # noqa

    # Import Receivers so that they are registered with mongoengine signals
    from app import receivers

    # Register web application routes
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register API routes
    from app.api.v1 import api_v1 as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    # Import celery task so that it is registered with the Celery workers
    from . import tasks # noqa
    # logger config
    package_name = '.'.join(__name__.split('.')[:-1])
    root_logger = logging.getLogger(package_name)
    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(console_handler)
    console_handler.setFormatter(log_formatter)
    app.logger.setLevel(current_config.LOG_LEVEL)
    # uncomment below three lines to enable file handler
    # rotating_file_handler = RotatingFileHandler(current_config.LOG_FILE_LOCATION, maxBytes=1024 * 1024 * 100, backupCount=20)
    # rotating_file_handler.setFormatter(log_formatter)
    # app.logger.addHandler(rotating_file_handler)

    app.logger.info("server environment : {}".format(config_name))

    return app
