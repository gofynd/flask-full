import logging
from app.customqueryset import CustomQuerySet
from app.signals import me_pre_update


logger = logging.getLogger(__name__)


@me_pre_update.connect_via(CustomQuerySet)
def on_pre_update_customqueryset_signal(sender, **kwargs):
    logger.debug("me_pre_update signal received from %r, data %r" % (sender, kwargs))
    logger.debug("kwargs after pre_update {}".format(kwargs))
    logger.debug('returning from pre_update receiver...')
    return 'received!'
#