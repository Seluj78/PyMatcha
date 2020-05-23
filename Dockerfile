FROM python:3.7

MAINTAINER Jules Lasne "jlasne@student.42.fr"

RUN apt-get update
RUN apt-get -y install apt-utils curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_12.x  | bash -
RUN apt-get -y install nodejs

WORKDIR /src

ADD . /src

RUN pip install -r backend/requirements.txt

RUN rm -rf www
RUN cp -R backend www
RUN npm i --prefix frontend
RUN npm run build --prefix frontend
RUN mkdir www/static
RUN mv frontend/build www/static

WORKDIR /src/www

ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER_COMPOSE true
EXPOSE 5000

CMD gunicorn --chdir . app:application -w 2 --threads 2 -b 0.0.0.0:5000
