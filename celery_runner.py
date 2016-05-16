from celery import Celery


app = Celery(
    'code',
    backend='amqp',
    broker='amqp://',
    include=['auto_tasks', 'mail'],  # include tasks, that will async run
)

app.config_from_object('celery_conf')

if __name__ == '__main__':
    app.start()
