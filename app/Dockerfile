FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential cmake libopenblas-dev liblapack-dev 
RUN pip install --upgrade pip
RUN pip install Flask gunicorn Pillow dlib numpy requests python-dotenv gevent flask-wtf

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --worker-class gevent --workers 3 --threads 16 --timeout 0 main:app

