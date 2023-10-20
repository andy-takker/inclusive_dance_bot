#! /usr/bin/env bash
alembic -c /app/src/alembic.ini upgrade head

python /app/src/initial_data.py