ARG VARIANT=3.12.8-slim-bookworm

# Base stage
FROM python:${VARIANT} AS base
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
RUN pip install pipenv

## Dev with mounted volumes and dev deps
FROM base AS dev
COPY Pipfile Pipfile.lock gunicorn.conf.py ./
RUN pipenv install --dev
CMD ["pipenv", "run", "gunicorn", "--reload", "app.api.main:app"]

## Prod with copied code and minimal deps
FROM base AS prod
COPY . .
RUN pipenv install --deploy
CMD ["pipenv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.api.main:app"]
