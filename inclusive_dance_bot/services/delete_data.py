from inclusive_dance_bot.db.uow.main import UnitOfWork
from inclusive_dance_bot.services.storage import Storage


async def delete_url_by_slug(uow: UnitOfWork, storage: Storage, url_slug: str) -> None:
    await uow.urls.delete_by_slug(url_slug=url_slug)
    await uow.commit()
    await storage.refresh_urls()
