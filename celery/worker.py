import os
from celery import Celery

CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
