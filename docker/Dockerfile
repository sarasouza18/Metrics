FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/metrics

COPY ../requirements ./requirements

RUN pip install --no-cache-dir -r requirements/dev.txt

COPY .. .

ENV PYTHONPATH=/app
ENV APP_ENV=production
ENV PROMETHEUS_MULTIPROC_DIR=/app/metrics

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "infrastructure.api.routes:app"]
