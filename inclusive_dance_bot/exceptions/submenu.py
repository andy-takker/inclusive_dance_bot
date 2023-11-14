from inclusive_dance_bot.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)


class SubmenuNotFoundError(EntityNotFoundError):
    pass


class SubmenuAlreadyExistsError(EntityAlreadyExistsError):
    pass
