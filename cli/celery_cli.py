import logging

import click
from celery.bin import worker
from celery import current_app as current_celery_app
from copy import deepcopy
from app import config_name, current_config
from manage import cli

logger = logging.getLogger(__name__)


@cli.command()
@click.option('--queues', help='comma sepereated list of queues worker will listen to')
@click.option('--logfile', help='logfile path')
@click.option('--concurrency', help='concurrency', type=int)
@click.option('--worker_max_tasks_per_child', help='worker_max_tasks_per_child', type=int)
def celery(queues, logfile, concurrency, worker_max_tasks_per_child):
    """Starts the celery worker."""
    config = deepcopy(current_config.CELERY_WORKER_CONFIG)

    if queues:
        config.update(queues=queues.split(','))
        logger.info("worker is listening to queues: {}".format(queues))
    else:
        logger.info("worker is listening to ALL queues")

    if logfile:
        config.update(logfile=logfile)
    if concurrency:
        config.update(concurrency=concurrency)
    if worker_max_tasks_per_child:
        config.update(worker_max_tasks_per_child=worker_max_tasks_per_child)

    application = current_celery_app._get_current_object()
    w = worker.worker(app=application)
    logger.info("celery environment : {}".format(config_name))
    w.run(**config)
