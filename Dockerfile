FROM python:3.11

RUN apt-get update && apt-get install -y postgresql

WORKDIR /backend

COPY poetry.lock pyproject.toml /backend/

# Install poetry dependency manager
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
RUN poetry --version

RUN poetry install --no-interaction --no-ansi

COPY . .

ENV PYTHONPATH=/backend

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
