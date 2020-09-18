FROM python:3.8.3-buster
WORKDIR /www
ADD backend/requirements.txt .
ADD .env .
RUN export $(cat .env | xargs)
RUN pip install -r requirements.txt
ADD backend .
ENV PYTHONDONTWRITEBYTECODE 1
EXPOSE 5000
CMD exec gunicorn --chdir /www --bind :5000 --workers 1 --threads 1 PyMatcha:application
