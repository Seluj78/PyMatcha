import logging

from flask_mail import Message
from PyMatcha import application
from PyMatcha import celery
from PyMatcha import mail


@celery.task
def send_mail_text(dest: str, subject: str, body: str, sender: str = "pymatcha@gmail.com"):
    msg = Message(subject=subject, body=body, sender=sender, recipients=[dest])
    with application.app_context():
        logging.debug("Sending text mail to {}.".format(dest))
        mail.send(msg)
        return "Mail sent successfully to {}.".format(dest)


@celery.task
def send_mail_html(dest: str, subject: str, html: str, sender: str = "pymatcha@gmail.com"):
    msg = Message(subject=subject, html=html, sender=sender, recipients=[dest])
    with application.app_context():
        logging.debug("Sending HTML mail to {}.".format(dest))
        mail.send(msg)
        return "Mail sent successfully to {}.".format(dest)
