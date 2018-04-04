from app import celery_app
from .base import BaseTask


class Task1(object):

    def run(self, *args, **kwargs):
        print("this is task 1")


@celery_app.task(bind=True, base=BaseTask, name='task_1')
def task_1(*args, **kwargs):
    Task1().run(*args, **kwargs)