class DomainError(Exception):
    """Base class for domain errors."""


class NotFoundError(DomainError):
    """Requested resource does not exist."""


class ConflictError(DomainError):
    """Request violates a uniqueness or state constraint."""


class InsufficientStockError(DomainError):
    """Not enough stock to satisfy an order."""
