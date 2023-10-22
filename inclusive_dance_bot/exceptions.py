class InclusiveDanceError(Exception):
    pass


class EntityNotFoundError(InclusiveDanceError):
    pass


class UrlAlreadyExistsError(InclusiveDanceError):
    pass


class UserTypeAlreadyExistsError(InclusiveDanceError):
    pass


class UrlSlugAlreadyExistsError(InclusiveDanceError):
    pass


class EntityAlreadyExistsError(InclusiveDanceError):
    pass


class UserAlreadyExistsError(InclusiveDanceError):
    pass


class UserTypeUserAlreadyExistsError(InclusiveDanceError):
    pass


class InvalidUserIDError(InclusiveDanceError):
    pass


class InvalidUserTypeIDError(InclusiveDanceError):
    pass
