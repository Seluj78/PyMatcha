import logging

from PyMatcha import mail, celery, application

from flask_mail import Message


@celery.task
def send_mail_text(dest: str, subject: str, body: str, sender: str = "pymatcha@gmail.com"):
    msg = Message(subject=subject, body=body, sender=sender, recipients=[dest])
    with application.app_context():
        logging.debug("Sending text mail to {}".format(dest))
        mail.send(msg)


@celery.task
def send_mail_html(dest: str, subject: str, body: str, sender: str = "pymatcha@gmail.com"):
    msg = Message(subject=subject, body=body, sender=sender, recipients=dest)
    with application.app_context():
        logging.debug("Sending HTML mail to {}".format(dest))
        mail.send(msg)
