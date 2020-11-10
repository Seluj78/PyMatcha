FROM python:3.8.3-buster
WORKDIR /www
ADD backend/requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en
ADD backend .
ENV PYTHONDONTWRITEBYTECODE 1
EXPOSE 5000
ADD .env .
RUN export $(cat .env | xargs)
CMD celery -A PyMatcha.celery worker -E --loglevel=INFO -B --pool=threads
