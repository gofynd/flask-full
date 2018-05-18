import logging

import click
import sys
from celery.bin import worker
from celery import current_app as current_celery_app
from copy import deepcopy

from celery.signals import after_setup_task_logger, after_setup_logger

from app import config_name, current_config, log_formatter
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


def create_celery_logger_handler(logger, propagate):
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    logger.logLevel = current_config.LOG_LEVEL
    logger.propagate = propagate


@after_setup_task_logger.connect
def after_setup_celery_task_logger(logger, **kwargs):
    """ This function sets the 'celery.task' logger handler and formatter """
    create_celery_logger_handler(logger, True)

@after_setup_logger.connect
def after_setup_celery_logger(logger, **kwargs):
    """ This function sets the 'celery' logger handler and formatter """
    create_celery_logger_handler(logger, False)