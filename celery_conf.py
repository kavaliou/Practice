from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'add-every-10-seconds': {
        'task': 'auto_tasks.add',
        'schedule': timedelta(seconds=20),
    },
}

CELERY_TASK_RESULT_EXPIRES = 3600
