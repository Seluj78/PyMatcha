FROM python:3.7

MAINTAINER Jules Lasne "jlasne@student.42.fr"

ADD www /www

WORKDIR /www

RUN pip install -r backend/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "backend/app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
ENV FLASK_SECRET_KEY "ThisIsADevelopmentKey"
ENV DB_USER "root"
ENV DB_ ""

EXPOSE 5000

CMD flask run --host=0.0.0.0