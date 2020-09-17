FROM python:3.8.3-buster
WORKDIR /www
ADD backend/requirements.txt .
ADD .env .
RUN export $(cat .env | xargs)
RUN pip install -r requirements.txt
ADD backend .
ENV PYTHONDONTWRITEBYTECODE 1
ENV IS_DOCKER_COMPOSE true
EXPOSE 5000
CMD gunicorn --chdir /www app:application -w 2 --threads 2 -b 0.0.0.0:5000
