#! /usr/bin/env bash
alembic -c /app/inclusive_dance_bot/alembic.ini upgrade head

python /app/inclusive_dance_bot/init_data.py