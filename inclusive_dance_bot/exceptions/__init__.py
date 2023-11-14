from inclusive_dance_bot.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InclusiveDanceError,
)
from inclusive_dance_bot.exceptions.mailing import MailingNotFoundError
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
    UserNotFoundError,
    UserTypeAlreadyExistsError,
    UserTypeUserAlreadyExistsError,
)

__all__ = (
    "InclusiveDanceError",
    "EntityAlreadyExistsError",
    "EntityNotFoundError",
    "MailingNotFoundError",
    "SubmenuAlreadyExistsError",
    "SubmenuNotFoundError",
    "UrlAlreadyExistsError",
    "UrlSlugAlreadyExistsError",
    "UrlNotFoundError",
    "UserAlreadyExistsError",
    "UserTypeAlreadyExistsError",
    "UserNotFoundError",
    "UserTypeUserAlreadyExistsError",
    "InvalidUserIDError",
    "InvalidUserTypeIDError",
)
