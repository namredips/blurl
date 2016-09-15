FROM python:3-alpine

MAINTAINER Jeff Cox <jeff@infiquetra.com>

ENV PYTHONUNBUFFERED 1
ARG DOCKERIZE_VER=v0.2.0

RUN apk add --no-cache curl &&\
  curl -fsL \
       https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VER/dockerize-linux-amd64-$DOCKERIZE_VER.tar.gz | \
       tar -C /usr/local/bin -zxvof - && \
  pip3 install falcon \
  gunicorn \
  markdown \
  pymongo

COPY . /api
WORKDIR /api
