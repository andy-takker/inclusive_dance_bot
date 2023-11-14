# Inclusive Dance Bot

## Stack

<a href="https://github.com/Ileriayo/markdown-badges">
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img alt="Postgres" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
    <img alt="Redis" src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white"/>
    <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    <img alt="GitHub Actions" src="https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white"/>
  </p>
</a>

## Description

Telegram bot for informing the audience and feedback. You can fully control the bot from the admin menu: change the displayed menus and messages, collect feedback and send out announcements on a schedule.

The bot was created completely asynchronous using [aiogram 3.0+](https://aiogram.dev/), [aiogram-dialogs 2.0+](https://aiogram-dialog.readthedocs.io/en/2.0.0/), [aiomisc](https://aiomisc.readthedocs.io/) and [sqalchemy](https://www.sqlalchemy.org/) libraries.

Initially, this project was developed to help the organization of [Inclusive Dance](https://inclusive-dance.ru/).

## Using

### Settings

Environment variables are used to configure the bot for connecting to Telegram, Postgres and Redis.

```bash

TELEGRAM_BOT_TOKEN      # your bot token
TELEGRAM_BOT_ADMIN_IDS  # Superadmin IDs, who can appoint other admins

DEBUG                   # Flag for debugging (using in sqlalchemy engine for echo)

POSTGRES_HOST           # database host
POSTGRES_PORT           # database port
POSTGRES_USER           # database user
POSTGRES_PASSWORD       # database password
POSTGRES_DB             # database name

REDIS_HOST              # redis host
REDIS_PORT              # redis port
REDIS_PASSWORD          # redis password
REDIS_DB                # redis db
```

### Docker

You can get image from public Docker Hub from [here](https://hub.docker.com/r/andytakker/inclusive_dance_bot).

```bash
docker pull andytakker/inclusive_dance_bot
```

### Local

Before you need to create env and install dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -U pip poetry
poetry install
```

For start the bot local you can use poetry

```bash
poetry run bot
```

### Test

For the main functions of the bot, tests are written using pytest. For running

```bash
pytest -vx ./tests/
```
