FROM python:3.7-alpine

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true
ENV PYTHONUNBUFFERED 1

COPY . /queue
WORKDIR /queue

RUN pip install -r requirements.txt

COPY ../backend .

ENTRYPOINT celery -A Pymatcha.celery -B --loglevel=debug