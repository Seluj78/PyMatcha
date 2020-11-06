import logging

from flask import has_request_context
from flask import request
from flask.logging import default_handler


class LoggingRequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def setup_logging():
    """
    Defines the logging configuration and prints a logging start message.
    """

    formatter = LoggingRequestFormatter(
        "%(asctime)s,%(msecs)d %(levelname)-8s "
        "[%(pathname)s:%(lineno)d (%(funcName)s()] [%(remote_addr)s requested %(url)s]"
        " %(process)d: %(message)s"
    )
    default_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d (%(funcName)s()] %(process)d:"
        " %(message)s",
        datefmt="%d-%m-%Y:%H:%M:%S",
    )

    logging.info("************************************************************")
    logging.info("************ Starting new instance of PyMatcha *************")
    logging.info("************************************************************")
