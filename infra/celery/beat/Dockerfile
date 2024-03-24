FROM python:3.10.12-slim

WORKDIR /wellbex_test

COPY ../../../poetry.lock pyproject.toml /wellbex_test/
COPY ../../.. /wellbex_test/
COPY ../../../env.example .env

RUN pip install --upgrade --no-cache-dir pip==24.0 && \
    pip install -U --no-cache-dir poetry==1.8 && \
    poetry config --local virtualenvs.create false && \
    poetry install

CMD ["celery", "-A", "core", "beat", "--loglevel=info"]
