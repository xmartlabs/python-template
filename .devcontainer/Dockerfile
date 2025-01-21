FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl libpq-dev gcc git

ENV POETRY_HOME="/usr/local" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.8.3

RUN curl -sSL https://install.python-poetry.org | python3 -
