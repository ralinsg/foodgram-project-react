FROM python:3.9-slim
LABEL author="ralinsg" version='0.1' release_date='28.02.2023'
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && pip install -r requirements.txt
COPY . ./
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
