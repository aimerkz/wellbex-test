FROM python:3.10.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /wellbex-test
COPY poetry.lock pyproject.toml /wellbex-test/

RUN pip install --upgrade --no-cache-dir pip==24.0 && \
    pip install -U --no-cache-dir poetry==1.8 && \
    poetry config --local virtualenvs.create false && \
    poetry install

COPY . /wellbex-test/
COPY env.example .env

RUN chmod a+x /wellbex-test/docker-entrypoint.sh
ENTRYPOINT ["/wellbex-test/docker-entrypoint.sh"]

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
