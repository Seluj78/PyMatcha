FROM python:3.7

MAINTAINER Jules Lasne "jlasne@student.42.fr"

#ADD ../www /www

#WORKDIR /www

WORKDIR /www

COPY requirements.txt /www

RUN pip install -r requirements.txt

ADD . /www

ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER_COMPOSE true
EXPOSE 5000

CMD gunicorn app:application -w 2 --threads 2 -b 0.0.0.0:5000 --log-level=debug