ARG VARIANT=3.12.8-slim-bookworm

# Base stage
FROM python:${VARIANT} AS base
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
RUN pip install pipenv==2024.4.0

## Dev with mounted volumes and dev deps
FROM base AS dev
COPY Pipfile Pipfile.lock ./
RUN pipenv install --dev
COPY gunicorn.conf.py pyproject.toml ./
VOLUME ["/app/app", "/app/data"]
CMD ["pipenv", "run", "gunicorn", "app.api.main:app"]

# Standalone dev with code included
FROM dev AS dev-standalone
COPY app ./app
COPY data ./data

## Prod with copied code and minimal deps
FROM base AS prod
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .
CMD ["gunicorn", "app.api.main:app"]
