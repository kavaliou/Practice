from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'run_task-every-20-seconds': {
        'task': 'auto_tasks.run_task',
        'schedule': timedelta(seconds=20),
    },
}

CELERY_TASK_RESULT_EXPIRES = 3600
