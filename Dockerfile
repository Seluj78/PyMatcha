FROM node:14.3-alpine3.10 AS frontend
WORKDIR /src
ADD frontend .
RUN npm i
ADD .env .
RUN export $(cat .env | xargs)
RUN npm run build

FROM python:3.8.3-buster
WORKDIR /www
ADD backend/requirements.txt .
ADD .env .
RUN export $(cat .env | xargs)
RUN pip install -r requirements.txt
ADD backend .
COPY --from=frontend /src/build frontend
ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER_COMPOSE true
EXPOSE 5000
CMD gunicorn --chdir /www app:application -w 2 --threads 2 -b 0.0.0.0:5000
