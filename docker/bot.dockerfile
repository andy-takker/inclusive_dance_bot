FROM python:3.11-slim
RUN pip install -U --no-cache-dir poetry pip && poetry config virtualenvs.create false

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi --no-root --without dev

COPY ./docker/pre-start.sh ./docker/start.sh /app/
RUN chmod +x /app/start.sh /app/pre-start.sh

COPY ./inclusive_dance_bot /app/inclusive_dance_bot

ENV PYTHONPATH=/app
CMD ["/app/start.sh"]