FROM mcr.microsoft.com/azureml/onnxruntime:v1.4.0

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential cmake libopenblas-dev liblapack-dev 
RUN pip install --upgrade pip
RUN pip install Flask gunicorn Pillow dlib

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app

