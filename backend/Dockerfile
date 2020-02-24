FROM python:3.7

MAINTAINER Jules Lasne "jlasne@student.42.fr"

#ADD ../www /www

#WORKDIR /www

COPY . /www

WORKDIR /www

RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER_COMPOSE true
EXPOSE 5000

CMD flask run --host=0.0.0.0