import logging
from copy import deepcopy

import click
from celery.bin import beat as beat_app
from celery import current_app as current_celery_app
from app import current_config, config_name
from app.crons import CELERYBEAT_SCHEDULE
from manage import cli

logger = logging.getLogger(__name__)


@cli.command()
@click.option('--logfile', help='logfile path')
@click.option('--concurrency', help='concurrency', type=int)
def beat(logfile, concurrency):
    """Starts the celery beat."""
    config = deepcopy(current_config.CELERY_BEAT_CONFIG)
    if logfile:
        config.update(logfile=logfile)
    if concurrency:
        config.update(concurrency=concurrency)

    application = current_celery_app._get_current_object()
    application.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)
    my_beat = beat_app.beat(app=application)
    logger.info("beat environment : {}".format(config_name))
    my_beat.run(**config)
