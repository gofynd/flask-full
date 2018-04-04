from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'task_1': {
        'task': 'task_1',
        'schedule': crontab(minute="*/1")
    }
}