from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from celery_runner import app


address = "tasky.itra@gmail.com"
pwd = "Itransition"


def connect_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(address, pwd)
    return server


@app.task()
def send(to, subject, message):
    server = connect_server()
    msg = MIMEMultipart()
    msg['From'] = address
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server.sendmail(address, to, msg.as_string())
    server.quit()
