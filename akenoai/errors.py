class IncorrectInputError(Exception):
    pass

class ForbiddenError(Exception):
    """Custom exception for 403/401 Forbidden"""
    pass

class InternalError(Exception):
    """Custom exception for 500 Error"""
    pass

__all__ = [
    "IncorrectInputError",
    "ForbiddenError",
    "InternalError"
]
