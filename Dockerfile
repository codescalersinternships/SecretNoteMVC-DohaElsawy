FROM python:3.12.3-alpine

ENV PYTHONUNBUFFERED=1
ENV MEMCACHED_HOST=memcached
ENV MEMCACHED_PORT=11211


WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000
