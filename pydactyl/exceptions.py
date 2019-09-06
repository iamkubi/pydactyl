"""Error classes for Pydactyl."""


class PydactylError(Exception):
    """Base error class."""


class BadRequestError(PydactylError):
    """Raised when a request is passed invalid parameters."""
    pass


class ClientConfigError(PydactylError):
    """Raised when a client configuration error exists."""
    pass
