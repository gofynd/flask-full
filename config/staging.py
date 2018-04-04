from .common import Config


class StagingConfig(Config):
    DEBUG = True
    IS_AUTH_ENABLED = False

    MEDIA_DIR = 'media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')
