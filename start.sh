#! /usr/bin/env bash
python -m inclusive_dance_bot.db --pg-url $PG_URL upgrade head

python /app/inclusive_dance_bot/init_data.py

python -m inclusive_dance_bot