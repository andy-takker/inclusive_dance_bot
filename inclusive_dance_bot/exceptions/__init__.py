from inclusive_dance_bot.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InclusiveDanceError,
)
from inclusive_dance_bot.exceptions.submenu import (
    SubmenuAlreadyExistsError,
    SubmenuNotFoundError,
)
from inclusive_dance_bot.exceptions.url import (
    UrlAlreadyExistsError,
    UrlNotFoundError,
    UrlSlugAlreadyExistsError,
)
from inclusive_dance_bot.exceptions.user import (
    InvalidUserIDError,
    InvalidUserTypeIDError,
    UserAlreadyExistsError,
    UserTypeAlreadyExistsError,
    UserTypeUserAlreadyExistsError,
)

__all__ = (
    "InclusiveDanceError",
    "EntityAlreadyExistsError",
    "EntityNotFoundError",
    "SubmenuAlreadyExistsError",
    "SubmenuNotFoundError",
    "UrlAlreadyExistsError",
    "UrlSlugAlreadyExistsError",
    "UrlNotFoundError",
    "UserAlreadyExistsError",
    "UserTypeAlreadyExistsError",
    "UserTypeUserAlreadyExistsError",
    "InvalidUserIDError",
    "InvalidUserTypeIDError",
)
