from inclusive_dance_bot.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)


class UrlAlreadyExistsError(EntityAlreadyExistsError):
    pass


class UrlSlugAlreadyExistsError(EntityAlreadyExistsError):
    pass


class UrlNotFoundError(EntityNotFoundError):
    pass
