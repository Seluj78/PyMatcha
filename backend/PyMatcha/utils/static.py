import os

FLASK_PORT = os.getenv("FLASK_PORT")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")
FLASK_HOST = os.getenv("FLASK_HOST")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

ENABLE_LOGGING = os.getenv("ENABLE_LOGGING")

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

DEBUG_AUTH_TOKEN = os.getenv("DEBUG_AUTH_TOKEN")

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

FRONTEND_EMAIL_CONFIRMATION_URL = FRONTEND_BASE_URL + "/accounts/verify?token="
FRONTEND_PASSWORD_RESET_URL = FRONTEND_BASE_URL + "/accounts/password/reset?token="

PYMATCHA_ROOT = os.path.join(os.path.dirname(__file__), "../..")
BACKEND_ROOT = os.path.join(os.path.dirname(__file__), "../")

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
IMGUR_CLIENT_SECRET = os.getenv("IMGUR_CLIENT_SECRET")

BOT_CONV_OPENERS = [
    "Hey baby, are you a microwave? Cause mmmmmmmmmmmmmmmmm",
    "How much does a polar bear weigh?",
    "Hi sexy",
    "Hello cutie",
    "Heyoooo",
]
