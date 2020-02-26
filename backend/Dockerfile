FROM python:3.7

MAINTAINER Jules Lasne "jlasne@student.42.fr"

WORKDIR /src

COPY backend/requirements.txt /src

RUN pip install -r requirements.txt

ADD . /src

WORKDIR /src

COPY Makefile /src

RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_12.x  | bash -
RUN apt-get -y install nodejs

RUN make docker_build

workdir /src/www

ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER_COMPOSE true
EXPOSE 5000

CMD gunicorn --chdir backend app:application -w 2 --threads 2 -b 0.0.0.0:5000 --log-level=debug