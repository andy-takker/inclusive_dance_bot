import os

import requests

MARKDOWN_MESSAGE_TEMPLATE = """
{message}

Triggered by {event_name}

[Action]({action_url})

[Repository]({repository_url})
"""


def send_message(
    token: str,
    title: str,
    message: str,
    event_name: str,
    action_url: str,
    repository_url: str,
) -> None:
    requests.post(
        url="http://188.225.87.124/message",
        params={"token": token},
        json={
            "title": title,
            "message": MARKDOWN_MESSAGE_TEMPLATE.format(
                message=message,
                event_name=event_name,
                action_url=action_url,
                repository_url=repository_url,
            ),
            "extras": {
                "client::display": {
                    "contentType": "text/markdown",
                }
            },
        },
    )


def main():
    token = os.getenv("GOTIFY_APP_TOKEN")
    event_name = os.getenv("GOTIFY_EVENT_NAME")
    action_url = os.getenv("GOTIFY_ACTION_URL")
    repository_url = os.getenv("GOTIFY_REPOSITORY_URL")
    title = os.getenv("GOTIFY_TITLE")
    message = os.getenv("GOTIFY_MESSAGE")

    send_message(
        token=token,
        title=title,
        repository_url=repository_url,
        action_url=action_url,
        event_name=event_name,
        message=message,
    )


if __name__ == "__main__":
    main()
