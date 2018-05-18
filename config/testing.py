import os
from app import app_name
from .common import Config


class TestingConfig(Config):
    TESTING = True
    IS_AUTH_ENABLED = False

    MEDIA_DIR = 'media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')
    LOG_FILE_LOCATION = '{}/{}'.format(os.getcwd(), 'temp/{}.log'.format(app_name))
