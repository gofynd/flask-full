import logging
import os

from pymongo import MongoClient,ReadPreference
from .common import Config


class ProductionConfig(Config):
    DEBUG = True
    MEDIA_DIR = 'media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')

    LOG_LEVEL = logging.INFO

    CELERY_WORKER_CONFIG = {
        'broker': Config.CELERY_BROKER_URL,
        'loglevel': LOG_LEVEL,
        'traceback': True,
        'worker_max_tasks_per_child': 50
    }

    CELERY_BEAT_CONFIG = {
        'broker': Config.CELERY_BROKER_URL,
        'loglevel': LOG_LEVEL,
        'traceback': True,
        'schedule': 'celerybeat-schedule.db'
    }
