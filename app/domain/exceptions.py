# app/domain/exceptions.py
class UnauthorizedAccessError(Exception):
    """Raised when user tries to access another user's data"""

class RateLimitExceededError(Exception):
    """Raised when rate limit is exceeded"""

class MetricsNotFoundError(Exception):
    """Raised when metrics are not found for a user"""