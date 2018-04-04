import os
from .common import Config


class PreProductionConfig(Config):
    DEBUG = True
    MEDIA_DIR = 'media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')
