FROM python:3.9.0-alpine
MAINTAINER nazarii.romanchenko@stemsc.com

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	LANG=C.UTF-8 \
	HOME=/usr/src/web
WORKDIR $HOME

# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev openssl libffi-dev openssl-dev \
	&& pip install --upgrade pip

COPY /requirements.txt  ./requirements.txt

RUN pip install -r ./requirements.txt

COPY ./docker/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./web $HOME
