import logging
from celery import Task
from flask_mail import Message

from app import current_config, config_name, mail

logger = logging.getLogger(__name__)


class BaseTask(Task):
    abstract = True

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(str(einfo))
        logger.debug("Task_id {} failed, Arguments are {}".format(task_id, args))

        if current_config.IS_ERROR_MAIL_ENABLED:
            # send error mail
            mail_subject = "[App Celery] for task_id {}, {}".format(task_id, str(exc))

            if config_name != 'production':
                mail_subject = "[App Celery {}] for task_id {}, {}".format(config_name, task_id, str(exc))

            mail_body = "\nargs: {} \nkwargs: {}\n\n\n {}".format(args, kwargs, (str(einfo)))
            msg = Message(subject=mail_subject, body=mail_body, sender=current_config.DEFAULT_MAIL_SENDER, recipients=current_config.ADMINS)
            mail.send(msg)

        # current_datetime = datetime.now()
        # datetime_str = str(current_datetime)
        # error_details_api_url = "{}celery-error-log/?datetime={}".format(current_config.SERVER_DOMAIN, datetime_str.replace(" ", '%20'))
        # error_message = "*Attention:*`Task Failed`\n>*Task Name:* {}\n>*Task_id:* {}\n>*Error Details api url:* {}\n".format(self.name, task_id, error_details_api_url)
        # CeleryErrorLog(task_id=task_id, args=str(args), datetime=current_datetime, kwargs=str(kwargs), error=str(einfo), is_active=True).save()
        # SlackUtil().send_message(current_config.SLACK_CHANNELS["celery_task"], error_message, "tergeo-task-bot")

