import subprocess
import json

from celery_runner import app

from mail import send


@app.task()
def run_task():
    with open('configurations/conf1.json') as config:
        config = json.load(config)
        for conf in config['configs']:
            process_configuration(conf)


def process_configuration(config):
    def parse_line(l):
        space_index = l.rfind(' ')
        return l[:space_index].strip(), int(l[space_index:].strip())

    subprocess_result = subprocess.Popen('%s' % config['conf'], stdout=subprocess.PIPE)

    danger, critical = {}, {}
    for line in subprocess_result.stdout.readlines():
        name, value = parse_line(line)
        danger_value = config.get('danger_values', {}).get(name)
        critical_value = config.get('critical_values', {}).get(name)
        if critical_value is not None and critical_value < value:
            critical[name] = value
        elif danger_value is not None and danger_value < value:
            danger[name] = value

    result_text = ''
    for name, value in critical.iteritems():
        result_text += 'Critical!!! %s = %s\n' % (name, value)
    if len(critical) > 0:
        restart_system.delay(config)
        result_text += 'System was restarting\n\n'
    for name, value in danger.iteritems():
        result_text += 'Danger!!! %s = %s\n' % (name, value)

    send_email_to_admins(config.get('admins', []), 'Report', result_text)


@app.task
def restart_system(config):
    restart_script = config.get('restart_system_script')
    if restart_script is not None:
        subprocess.Popen(restart_script)


def send_email_to_admins(admins, subject, message):
    for admin in admins:
        send(admin, subject, message)
