#! /usr/bin/env bash
python -m idb.db --pg-url $PG_URL upgrade head

python /app/idb/init_data.py

python -m idb