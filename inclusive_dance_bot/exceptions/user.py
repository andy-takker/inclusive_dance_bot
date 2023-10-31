from inclusive_dance_bot.exceptions.base import (
    EntityAlreadyExistsError,
    InclusiveDanceError,
)


class UserAlreadyExistsError(EntityAlreadyExistsError):
    pass


class UserTypeUserAlreadyExistsError(EntityAlreadyExistsError):
    pass


class InvalidUserIDError(InclusiveDanceError):
    pass


class InvalidUserTypeIDError(InclusiveDanceError):
    pass


class UserTypeAlreadyExistsError(EntityAlreadyExistsError):
    pass
