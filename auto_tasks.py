import subprocess
import json

from celery_runner import app

from mail import send


@app.task()
def add():
    with open('configurations/conf1.json') as config:
        config = json.load(config)
        for conf in config['configs']:
            s = subprocess.Popen('%s' % conf['conf'], stdout=subprocess.PIPE)
            for line in s.stdout.readlines():
                space_index = line.rfind(' ')
                name = line[:space_index].strip()
                value = int(line[space_index:].strip())
                danger_value = conf['danger_values'].get(name)
                if danger_value is not None and danger_value < value:
                    send.delay(conf.get('admins')[0], 'Danger', '!!! %s %s' % (name, value))
