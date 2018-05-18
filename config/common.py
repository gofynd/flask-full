import os
import logging
from pymongo import ReadPreference
from app import app_name, redis_host, mongo_host
import redbeat

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    REDIS_DOMAIN = 'redis://{}:6379'.format(redis_host)
    AUTH_REDIS_URL = 'redis://{}:6379/0'.format(redis_host)

    DEBUG = False
    TESTING = False
    IS_AUTH_ENABLED = True
    IS_ERROR_MAIL_ENABLED = False

    LOG_LEVEL = logging.DEBUG

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '51f52814-0071-11e6-a247-000ec6c2372c')
    REQUEST_STATS_WINDOW = 15

    CELERY_BROKER_URL = '{}/{}'.format(REDIS_DOMAIN, 1)

    CELERY_RESULT_BACKEND = '{}/{}'.format(REDIS_DOMAIN, 1)

    CELERY_WORKER_CONFIG = {
        'broker': CELERY_BROKER_URL,
        'loglevel': LOG_LEVEL,
        'traceback': True,
        'worker_max_tasks_per_child': 50
    }


    REDBEAT_REDIS_URL = '{}/{}'.format(REDIS_DOMAIN, 3)
    REDBEAT_KEY_PREFIX = 'redbeat'
    REDBEAT_LOCK_KEY = 'redbeat:lock'
    # REDBEAT_LOCK_TIMEOUT = 2

    CELERY_BEAT_CONFIG = {
        'broker': CELERY_BROKER_URL,
        'loglevel': LOG_LEVEL,
        'traceback': True,
        'scheduler_cls': redbeat.RedBeatScheduler,
    }

    CELERY_DEFAULT_QUEUE = 'default'

    CELERY_QUEUES = {
        'default': {
            "exchange": "default",
            "binding_key": "default",
        },
        'queue1': {
            'exchange': 'queue1',
            'routing_key': 'queue1',
        },
        'queue2': {
            'exchange': 'queue2',
            'routing_key': 'queue2',
        },
        'queue3': {
            'exchange': 'queue3',
            'routing_key': 'queue3',
        },
        'queue4': {
            'exchange': 'queue4',
            'routing_key': 'queue4',
        },
        'queue5': {
            'exchange': 'queue5',
            'routing_key': 'queue5',
        }
    }

    # CELERY_ROUTES = {}

    CELERYD_TASK_SOFT_TIME_LIMIT = 120

    SOCKETIO_MESSAGE_QUEUE = os.environ.get('CELERY_BROKER_URL', 'redis://')

    MONGO_DATABASES = {
        "app": {
            "username": "user",
            "password": "password",
            "port": 27017,
            "host": "mongodb://user:password@{}/{}?authSource=admin".format(mongo_host, app_name),
            "db": "{}".format(app_name),
            "read_preference": ReadPreference.PRIMARY,
        }
    }

    MEDIA_DIR = '/media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')
    TEMP_DIR = '{}/{}'.format(BASE_DIR, 'temp')

    SLACK_TOKEN = "slacktoken"

    SLACK_CHANNELS = {
        "sync_issues": "test_channel",
        "content": "test_channel",
        "celery_task": "test_channel",
        "exceptions": "test_channel",
        "content_alert": "test_channel"
    }

    LOG_FILE_LOCATION = '/var/log/{}/{}.log'.format(app_name, app_name)

    CACHE_CONFIG = {
        'CACHE_TYPE': 'redis',
        'CACHE_KEY_PREFIX': 'fcache_',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': '6379',
        'CACHE_REDIS_URL': '{}/{}'.format(REDIS_DOMAIN, 2)
    }

    ADMINS = ['neerajshukla1911@gmail.com']

    CONTENT_ISSUES_EMAIL_IDS = []

