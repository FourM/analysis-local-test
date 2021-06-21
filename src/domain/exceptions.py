# TODO: considering error response format


class DomainException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class MissingEnvironmentVariableException(DomainException):
    ...


class MissingFileDataException(DomainException):
    ...


class ValidationException(DomainException):
    ...


class APIRequestException(DomainException):
    ...
