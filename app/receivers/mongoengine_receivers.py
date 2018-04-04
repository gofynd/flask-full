import logging
from mongoengine import signals
from app import signals as custom_signals

logger = logging.getLogger(__name__)


@signals.pre_save.connect
def on_pre_save_signal(sender, **kwargs):
    logger.debug("pre_save signal by {} and kwargs are {}".format(sender, kwargs))
    custom_signals.me_pre_update.send(sender, **kwargs)


@signals.post_save.connect
def on_post_save_signal(sender, **kwargs):
    logger.debug("post_update  signal from %r, data %r" % (sender, kwargs))
    custom_signals.me_post_update.send(sender, **kwargs)


@signals.pre_bulk_insert.connect
def on_pre_bulk_insert_signal(sender, **kwargs):
    logger.debug("pre_bulk_insert signal from %r, data %r" % (sender, kwargs))
    custom_signals.me_pre_update.send(sender, **kwargs)


@signals.post_bulk_insert.connect
def on_post_bulk_insert_signal(sender, **kwargs):
    logger.debug("post_bulk_insert signal from %r, data %r" % (sender, kwargs))
    custom_signals.me_post_update.send(sender, **kwargs)
