#! /usr/bin/env bash
set -e

python -m idb.db upgrade head

python /app/inutils/init_data.py --init-data-path=/app/inutils/init_data.yaml

python -m idb