from flask import Flask, jsonify
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from controllers.user_controller import user_bp
from config.logging_config import setup_logging, RequestLogging
from monitoring.metrics import track_request_metrics
from monitoring.rate_limiter import create_limiter, setup_error_handler, RATE_LIMITS
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Setup rate limiter
limiter = create_limiter()
limiter.init_app(app)

# Setup error handler for rate limiting
setup_error_handler(limiter, app)

# Setup request logging
RequestLogging(app)

# Setup metrics tracking
track_request_metrics(app)

# Register blueprints
app.register_blueprint(user_bp)

# Apply rate limiting to specific endpoints
try:
    limiter.limit(RATE_LIMITS["login"])(app.view_functions["user_bp.login"])
    limiter.limit(RATE_LIMITS["logout"])(app.view_functions["user_bp.logout"])
    limiter.limit(RATE_LIMITS["refresh"])(app.view_functions["user_bp.refresh"])
    limiter.limit(RATE_LIMITS["get_users"])(app.view_functions["user_bp.get_users"])
    limiter.limit(RATE_LIMITS["create_user"])(app.view_functions["user_bp.create_user"])
    limiter.limit(RATE_LIMITS["update_user"])(app.view_functions["user_bp.update_user"])
    limiter.limit(RATE_LIMITS["delete_user"])(app.view_functions["user_bp.delete_user"])
    logger.info("Rate limiting applied to all endpoints")
except Exception as e:
    logger.warning(f"Could not apply all rate limits: {str(e)}")


# Metrics endpoint (Prometheus scrape target)
@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Prometheus metrics endpoint
    """
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint
    """
    logger.debug("Health check called")
    return (
        jsonify(
            {"status": "healthy", "service": "User Management API", "version": "1.0.0"}
        ),
        200,
    )


if __name__ == "__main__":
    port = 5000
    logger.info(f"Starting server on port {port}")
    print(f"Server running at http://localhost:{port}")
    print(f"Metrics available at http://localhost:{port}/metrics")
    print(f"Health check at http://localhost:{port}/health")
    app.run(port=port, debug=False)
