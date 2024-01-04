from idb.exceptions.base import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    InclusiveDanceError,
)
from idb.exceptions.mailing import MailingNotFoundError
from idb.exceptions.submenu import (
    SubmenuAlreadyExistsError,
    SubmenuNotFoundError,
)
from idb.exceptions.url import (
    UrlAlreadyExistsError,
    UrlNotFoundError,
    UrlSlugAlreadyExistsError,
)
from idb.exceptions.user import (
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
