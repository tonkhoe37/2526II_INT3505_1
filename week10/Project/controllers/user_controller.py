from flask import Blueprint, request, jsonify, make_response
from services import user_service
from authentication.auth import auth_required
from authentication.blacklistToken import blacklistToken
from authorization.auth import role_required
from data.role_enum import Role
from monitoring.rate_limiter import RATE_LIMITS
from monitoring.metrics import LOGIN_ATTEMPTS, TOKEN_REFRESH, USER_OPERATIONS
import jwt
import datetime
import os
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

user_bp = Blueprint("user_bp", __name__)


def require_rate_limit(limiter, limit_string):
    """
    Decorator to apply rate limiting
    """

    def decorator(f):
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        decorated_function.__name__ = f.__name__
        # The limiter will be applied when the app is initialized
        return decorated_function

    return decorator


# LOGOUT
@user_bp.route("/logout", methods=["POST"])
@auth_required
def logout():
    try:
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        blacklistToken.add(token)

        logger.info(f"User logged out successfully")

        return jsonify({"message": "Logged out successfully"}), 200

    except Exception as e:
        logger.error(f"Logout failed: {str(e)}", exc_info=True)
        return jsonify({"error": "Logout failed"}), 500


# LOGIN
@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            LOGIN_ATTEMPTS.labels(status="failed").inc()
            return jsonify({"error": "Invalid data"}), 400

        email = data.get("email")
        password = data.get("password")

        user = user_service.login(email, password)

        if user is None:
            LOGIN_ATTEMPTS.labels(status="failed").inc()
            logger.warning(f"Login failed for email: {email}")
            return jsonify({"error": "Invalid credentials"}), 401

        now = datetime.datetime.utcnow()

        # Access token (ngắn hạn)
        access_token = jwt.encode(
            {
                "email": user.email,
                "role": user.role.name,
                "iat": now,
                "exp": now + datetime.timedelta(minutes=15),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        # Refresh token (dài hạn)
        refresh_token = jwt.encode(
            {
                "email": user.email,
                "iat": now,
                "exp": now + datetime.timedelta(days=7),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        LOGIN_ATTEMPTS.labels(status="success").inc()
        logger.info(f"User logged in successfully: {email}")

        return (
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_in": 900,
                }
            ),
            200,
        )

    except Exception as e:
        LOGIN_ATTEMPTS.labels(status="failed").inc()
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({"error": "Login failed"}), 500


# REFRESH
@user_bp.route("/refresh", methods=["POST"])
def refresh():
    try:
        data = request.get_json()

        if not data or "refresh_token" not in data:
            TOKEN_REFRESH.labels(status="failed").inc()
            return jsonify({"error": "Refresh token required"}), 400

        token = data.get("refresh_token")

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            new_access_token = jwt.encode(
                {
                    "email": decoded["email"],
                    "role": decoded["role"],
                    "iat": datetime.datetime.utcnow(),
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                },
                SECRET_KEY,
                algorithm="HS256",
            )

            TOKEN_REFRESH.labels(status="success").inc()
            logger.info(f"Token refreshed for: {decoded.get('email')}")

            return jsonify({"access_token": new_access_token, "expires_in": 900}), 200

        except jwt.ExpiredSignatureError:
            TOKEN_REFRESH.labels(status="failed").inc()
            logger.warning("Refresh token expired")
            return jsonify({"error": "Refresh token expired"}), 401

        except jwt.InvalidTokenError:
            TOKEN_REFRESH.labels(status="failed").inc()
            logger.warning("Invalid refresh token")
            return jsonify({"error": "Invalid refresh token"}), 401

    except Exception as e:
        TOKEN_REFRESH.labels(status="failed").inc()
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        return jsonify({"error": "Token refresh failed"}), 500


# CRUD USER
@user_bp.route("/users", methods=["GET"])
@auth_required
def get_users():
    try:
        users = user_service.get_users()

        USER_OPERATIONS.labels(operation="read", status="success").inc()
        logger.debug(f"Retrieved {len(users)} users")

        response = make_response(jsonify([u.to_dict() for u in users]))

        return response, 200

    except Exception as e:
        USER_OPERATIONS.labels(operation="read", status="failed").inc()
        logger.error(f"Get users error: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to retrieve users"}), 500


@user_bp.route("/users", methods=["POST"])
@auth_required
@role_required(Role.ADMIN)
def create_user():
    try:
        data = request.get_json()

        if not data:
            USER_OPERATIONS.labels(operation="create", status="failed").inc()
            return jsonify({"error": "Invalid data"}), 400

        user = user_service.create_user(data)

        if user is None:
            USER_OPERATIONS.labels(operation="create", status="failed").inc()
            logger.warning(f"Failed to create user: ID already exists")
            return jsonify({"error": "User ID already exists"}), 400

        USER_OPERATIONS.labels(operation="create", status="success").inc()
        logger.info(f"User created: {user.email}")

        return jsonify(user.to_dict()), 201

    except Exception as e:
        USER_OPERATIONS.labels(operation="create", status="failed").inc()
        logger.error(f"Create user error: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to create user"}), 500


@user_bp.route("/users/<id>", methods=["PUT"])
@auth_required
@role_required(Role.ADMIN)
def update_user(id):
    try:
        data = request.get_json()

        user = user_service.update_user(id, data)

        if user is None:
            USER_OPERATIONS.labels(operation="update", status="failed").inc()
            logger.warning(f"Failed to update user: ID {id} not found")
            return "", 404

        USER_OPERATIONS.labels(operation="update", status="success").inc()
        logger.info(f"User updated: {user.email}")

        return jsonify(user.to_dict()), 200

    except Exception as e:
        USER_OPERATIONS.labels(operation="update", status="failed").inc()
        logger.error(f"Update user error: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to update user"}), 500


@user_bp.route("/users/<id>", methods=["DELETE"])
@auth_required
@role_required(Role.ADMIN)
def delete_user(id):
    try:
        result = user_service.delete_user(id)

        if not result:
            USER_OPERATIONS.labels(operation="delete", status="failed").inc()
            logger.warning(f"Failed to delete user: ID {id} not found")
            return "", 404

        USER_OPERATIONS.labels(operation="delete", status="success").inc()
        logger.info(f"User deleted: ID {id}")

        return "", 204

    except Exception as e:
        USER_OPERATIONS.labels(operation="delete", status="failed").inc()
        logger.error(f"Delete user error: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to delete user"}), 500
