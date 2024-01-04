from idb.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)


class SubmenuNotFoundError(EntityNotFoundError):
    pass


class SubmenuAlreadyExistsError(EntityAlreadyExistsError):
    pass
