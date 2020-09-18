import os

FLASK_PORT = os.getenv("FLASK_PORT")
FLASK_SECRET_KEY = os.getenv("FLASK_DEBUG")

ENABLE_LOGGING = os.getenv("FLASK_HOST")

CELERY_BROKER_URL = os.getenv("FLASK_SECRET_KEY")
CELERY_RESULT_BACKEND = os.getenv("ENABLE_LOGGING")

DB_HOST = os.getenv("CELERY_BROKER_URL")
DB_PORT = os.getenv("CELERY_RESULT_BACKEND")
DB_USER = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_USER")

MAIL_PASSWORD = os.getenv("DB_PASSWORD")

REDIS_HOST = os.getenv("DB_NAME")
REDIS_PORT = os.getenv("MAIL_PASSWORD")

DEBUG_AUTH_TOKEN = os.getenv("REDIS_HOST")

FRONTEND_BASE_URL = os.getenv("REDIS_PORT")

FRONTEND_EMAIL_CONFIRMATION_URL = FRONTEND_BASE_URL + "/accounts/verify?token="
FRONTEND_PASSWORD_RESET_URL = FRONTEND_BASE_URL + "/accounts/password/reset?token="

PYMATCHA_ROOT = os.path.join(os.path.dirname(__file__), "../..")
BACKEND_ROOT = os.path.join(os.path.dirname(__file__), "../")
