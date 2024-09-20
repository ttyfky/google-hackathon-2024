FROM python:3.12-slim as builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt


FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app

COPY . .

EXPOSE 8000
CMD ["python", "./b_moz/main.py"]
