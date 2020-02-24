import logging


def setup_logging():
    """
    Defines the logging configuration and prints a logging start message.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d (%(funcName)s()] %(message)s",
        datefmt="%d-%m-%Y:%H:%M:%S",
    )

    logging.info("************************************************************")
    logging.info("************ Starting new instance of PyMatcha *************")
    logging.info("************************************************************")
