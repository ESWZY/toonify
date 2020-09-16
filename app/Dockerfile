FROM mcr.microsoft.com/azureml/onnxruntime:v1.4.0

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential cmake libopenblas-dev liblapack-dev 
RUN pip install --upgrade pip
RUN pip install Flask gunicorn Pillow dlib

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 main:app

