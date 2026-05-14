from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def create_limiter():
    """
    Tạo rate limiter instance
    """
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )

    return limiter


def setup_error_handler(limiter, app):
    """
    Cấu hình error handler cho rate limiter
    """

    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning(
            f"Rate limit exceeded",
            extra={
                "remote_addr": get_remote_address(),
                "path": app.request.path,
                "limit": str(e.limit),
            },
        )

        # Track rate limit hit
        from monitoring.metrics import RATE_LIMIT_HITS

        RATE_LIMIT_HITS.labels(endpoint=app.request.endpoint or "unknown").inc()

        return (
            jsonify(
                {
                    "error": "Rate limit exceeded",
                    "message": "Too many requests. Please try again later.",
                }
            ),
            429,
        )


# Định nghĩa các rate limit khác nhau cho các endpoint
RATE_LIMITS = {
    # Authentication endpoints - strict
    "login": "5 per minute",
    "refresh": "10 per minute",
    "logout": "30 per minute",
    # CRUD operations - moderate
    "get_users": "30 per minute",
    "create_user": "5 per minute",
    "update_user": "10 per minute",
    "delete_user": "5 per minute",
    # Profile - moderate
    "get_profile": "60 per minute",
    "update_profile": "10 per minute",
}
