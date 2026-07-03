# TODO: pin base image version
FROM python:3.12-slim

WORKDIR /app

# system deps for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# create non-root user
RUN useradd -m appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# change ownership
RUN chown -R appuser:appuser /app
USER appuser

CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info"]
