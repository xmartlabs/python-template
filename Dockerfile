FROM python:3.11

RUN apt-get update && apt-get install -y postgresql

# Install poetry dependency manager
ENV POETRY_HOME="/usr/local" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.8.3

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml /backend/

WORKDIR /backend

RUN poetry install --no-ansi

COPY . .

ENV PYTHONPATH=/backend

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
