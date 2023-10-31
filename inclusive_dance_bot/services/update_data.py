from typing import Any

from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.dto import UrlDto
from inclusive_dance_bot.services.storage import Storage


async def update_url_by_slug(
    uow: UnitOfWork,
    storage: Storage,
    url_slug: str,
    **kwargs: Any,
) -> UrlDto:
    url = await uow.urls.update_by_slug(url_slug=url_slug, **kwargs)
    await uow.commit()
    await storage.refresh_urls()
    return url
