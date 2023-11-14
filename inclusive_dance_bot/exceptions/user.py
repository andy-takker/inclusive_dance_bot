from inclusive_dance_bot.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InclusiveDanceError,
)


class UserAlreadyExistsError(EntityAlreadyExistsError):
    pass


class UserNotFoundError(EntityNotFoundError):
    pass


class UserTypeUserAlreadyExistsError(EntityAlreadyExistsError):
    pass


class InvalidUserIDError(InclusiveDanceError):
    pass


class InvalidUserTypeIDError(InclusiveDanceError):
    pass


class UserTypeAlreadyExistsError(EntityAlreadyExistsError):
    pass
