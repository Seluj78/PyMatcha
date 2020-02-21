from PyMatcha import mail

from flask_mail import Message


def send_mail_text(dest: str, subject: str, body: str, sender: str = "pymatcha@gmail.com"):
    msg = Message(subject=subject, body=body, sender=sender, recipients=[dest])
    mail.send(msg)


def send_mail_html(dest: str, subject: str, body: str, sender: str = "pymatcha@gmail.com"):
    msg = Message(subject=subject, body=body, sender=sender, recipients=dest)
    mail.send(msg)
