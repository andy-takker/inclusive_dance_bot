FROM python:3.11-slim
RUN pip install -U --no-cache-dir poetry pip && poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi --no-root --without dev

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
COPY /start.sh /app/
RUN chmod +x /app/start.sh /wait-for-it.sh

COPY ./inclusive_dance_bot /app/inclusive_dance_bot

ENV PYTHONPATH=/app
