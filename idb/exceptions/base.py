class InclusiveDanceError(Exception):
    pass


class EntityNotFoundError(InclusiveDanceError):
    pass


class EntityAlreadyExistsError(InclusiveDanceError):
    pass
