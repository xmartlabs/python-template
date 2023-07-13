FROM python:3.11

RUN apt-get update && apt-get install -y postgresql

WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV PYTHONPATH=/backend

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
