from prometheus_client import Counter, Histogram, Gauge
from flask import request, g
import time
import logging

logger = logging.getLogger(__name__)

# Request metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Tổng số request HTTP",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Thời gian xử lý request (giây)",
    ["method", "endpoint"],
)

# Authentication metrics
LOGIN_ATTEMPTS = Counter(
    "login_attempts_total",
    "Tổng số lần login",
    ["status"],
)

TOKEN_REFRESH = Counter(
    "token_refresh_total",
    "Tổng số lần refresh token",
    ["status"],
)

# Business metrics
USER_OPERATIONS = Counter(
    "user_operations_total",
    "Tổng số user operations",
    ["operation", "status"],
)

# Rate limit metrics
RATE_LIMIT_HITS = Counter(
    "rate_limit_hits_total",
    "Tổng số lần bị rate limit",
    ["endpoint"],
)

# Active connections
ACTIVE_CONNECTIONS = Gauge(
    "active_connections",
    "Số lượng kết nối đang hoạt động",
)


def track_request_metrics(app):
    """
    Middleware để track request metrics
    """

    @app.before_request
    def before_request():

        ACTIVE_CONNECTIONS.inc()

        # request-scoped variable
        g.start_time = time.time()

    @app.after_request
    def after_request(response):

        ACTIVE_CONNECTIONS.dec()

        if hasattr(g, "start_time"):

            duration = time.time() - g.start_time

            endpoint = request.endpoint or "unknown"

            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=endpoint,
                status=response.status_code,
            ).inc()

            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=endpoint,
            ).observe(duration)

            logger.debug(
                f"Request metrics: "
                f"{request.method} "
                f"{request.path} - "
                f"{response.status_code} "
                f"({duration:.3f}s)"
            )

        return response
