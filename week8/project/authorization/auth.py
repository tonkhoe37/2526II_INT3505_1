from flask import request, jsonify
from functools import wraps


def role_required(role):

    def wrapper(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            user = getattr(request, "user", None)

            if not user or user.get("role") != role.name:
                return jsonify({"error": "Forbidden"}), 403

            return f(*args, **kwargs)

        return decorated

    return wrapper
