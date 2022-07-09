FROM python:3.9-slim-buster

WORKDIR /usr/src

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install

RUN pip3 install --upgrade pip
COPY ./requirements.txt /usr/src/
RUN pip3 install -r requirements.txt

COPY . /usr/src/